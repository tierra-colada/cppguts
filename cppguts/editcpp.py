import argparse
import os
import shutil
import warnings

from clang.cindex import Cursor, CursorKind, Index
from pprint import pprint


def get_diag_info(diag):
    return {'severity': diag.severity,
            'location': diag.location,
            'category_name': diag.category_name,
            'spelling': diag.spelling,
            'ranges': diag.ranges,
            'fixits': diag.fixits}


def find_include_directives(txtdata: list) -> (list, list):
    '''
    Find lines and their indexes that has `#include` directives
    :param txtdata: list of str with data
    :return: includeidx, includelines - line indexes and lines
    '''
    includeidx = []
    includelines = []
    i = 0
    for line in txtdata:
        if line.strip().startswith('#') and line.strip()[1:].strip().lower().startswith("include"):
            includeidx.append(i)
            includelines.append(line)
        i += 1
    return includeidx, includelines


def generate_unique_filename(filenames: list, filename: str) -> str:
    '''
    Generates unique filename by adding `_i` to the name.
    For example: `myfile.cpp` becomes `myfile_1.cpp`.
    :param filenames: list of filenames that resides in the folder
    :param filename: base name for a file
    :return: uniquename - filename with unique name
    '''
    basename, extension = os.path.splitext(filename)
    uniquename = filename
    isunique = True
    i = 0
    while True:
        for name in filenames:
            if name.lower() == uniquename.lower():
                isunique = False
                break
        if isunique:
            return uniquename
        uniquename = basename + '_' + str(i) + extension
        isunique = True
        i += 1


def prepare_filename(destfile: str) -> str:
    '''
    Prepare unique filename.
    :param destfile: file name where it is expected it shoud be
    :return: prepared_filename - full path to the NOT yet created file
    '''
    destdir = os.path.dirname(os.path.abspath(destfile))
    filenames = [f for f in os.listdir(destdir) if os.path.isfile(os.path.join(destdir, f))]
    filename = os.path.basename(destfile)
    uniquename = generate_unique_filename(filenames, filename)
    prepared_filename = os.path.join(destdir, uniquename)
    return prepared_filename


def copy_file(srcfile: str, destfile: str) -> str:
    '''
    Copies `fromfile` to `tofile`. You must be confident that `tofile` doesn't exist yet.
    :param srcfile: file name to be copied
    :param destfile: file name where to copy
    :return: copiedfile - full path to the copied file
    '''
    destdir = os.path.dirname(os.path.abspath(destfile))
    filenames = [f for f in os.listdir(destdir) if os.path.isfile(os.path.join(destdir, f))]
    filename = os.path.basename(destfile)
    uniquename = generate_unique_filename(filenames, filename)
    copiedfile = os.path.join(destdir, uniquename)
    shutil.copy(srcfile, copiedfile)
    return copiedfile


def find_method_def_nodes(node: Cursor, nodes_found: list, location_filename=str()):
    try:
        if location_filename:
            if (node.kind == CursorKind.CXX_METHOD and node.is_definition() and
                    os.path.samefile(node.location.file.name, location_filename)):
                nodes_found.append(node)
            elif (node.kind == CursorKind.FUNCTION_DECL and node.is_definition() and
                  os.path.samefile(node.location.file.name, location_filename)):
                nodes_found.append(node)
            else:
                for child in node.get_children():
                    find_method_def_nodes(child, nodes_found, location_filename)
        else:
            if node.kind == CursorKind.CXX_METHOD and node.is_definition():
                nodes_found.append(node)
            elif node.kind == CursorKind.FUNCTION_DECL and node.is_definition():
                nodes_found.append(node)
            else:
                for child in node.get_children():
                    find_method_def_nodes(child, nodes_found, location_filename)
    except ValueError as e:
        msg = "Warning:\n" \
              "an exception were raised by libclang\n" \
              "node spelling:\t" + node.spelling + "\n" + \
              "node display:\t" + node.displayname + "\n" + \
              "node mangled name:\t" + node.mangled_name + "\n" + \
              "node location filename:\t" + node.location.file.name + "\n"
        warnings.warn(msg, RuntimeWarning)
        print("raised exception:\t", e)
        for child in node.get_children():
            find_method_def_nodes(child, nodes_found, location_filename)


def find_method_matching_node(reference_node: Cursor, nodes: list) -> Cursor:
    if reference_node:
        for node in nodes:
            if compare_method_nodes(reference_node, node):
                return node


def compare_method_nodes(node_1: Cursor, node_2: Cursor) -> bool:
    try:
        if (node_1.kind == node_2.kind and
                node_1.is_definition() == node_2.is_definition() and
                node_1.is_const_method() == node_2.is_const_method() and
                node_1.is_virtual_method() == node_2.is_virtual_method() and
                node_1.is_static_method() == node_2.is_static_method() and
                node_1.spelling == node_2.spelling and
                node_1.type.spelling == node_2.type.spelling):
            # if parent of one of the comparable FUNCTION is the filename than
            # we must not compare their parent as they belongs to different files
            if (node_1.kind == CursorKind.FUNCTION_DECL and
                    node_2.kind == CursorKind.FUNCTION_DECL and
                    node_1.semantic_parent.kind == CursorKind.TRANSLATION_UNIT and
                    node_2.semantic_parent.kind == CursorKind.TRANSLATION_UNIT):
                return True
            else:
                return node_1.semantic_parent.displayname == node_2.semantic_parent.displayname
    except ValueError as e:
        msg = "Warning:\n" \
              "an exception were raised by libclang\n" \
              "node_1 spelling:\t" + node_1.spelling + "\n" + \
              "node_2 spelling:\t" + node_2.spelling + "\n" + \
              "node_1 display:\t" + node_1.displayname + "\n" + \
              "node_2 display:\t" + node_2.displayname + "\n" + \
              "node_1 mangled name:\t" + node_1.mangled_name + "\n" + \
              "node_2 mangled name:\t" + node_2.mangled_name + "\n" + \
              "node_1 location filename:\t" + node_1.location.file.name + "\n" + \
              "node_2 location filename:\t" + node_2.location.file.name + "\n"
        warnings.warn(msg, RuntimeWarning)
        print("raised exception:\t", e)

    return False


# Comparing types is more difficult than I expected. Two classes with same name
# but that have different member vars have different `objc_type_encoding`
def compare_method_argument_types(node_1: Cursor, node_2: Cursor) -> bool:
    node_1_args = []
    for method_arg in node_1.get_arguments():
        node_1_args.append(method_arg)

    node_2_args = []
    for method_arg in node_2.get_arguments():
        node_2_args.append(method_arg)

    if len(node_1_args) != len(node_2_args):
        return False

    is_equal = True
    for i in range(0, len(node_1_args)):
        if node_1_args[i].objc_type_encoding != node_2_args[i].objc_type_encoding:
            is_equal = False
            break
    return is_equal


def main():
    parser = argparse.ArgumentParser(description=
                                     'Replace C++ function/method definition in destination file '
                                     '(but doesn`t work with templates). '
                                     'One source file may contain several functions/methods to replace. '
                                     'After passing `editcpp` flags you are allowed to pass clang '
                                     'commands like `-I` (to include dir), `-std=c++17` and other. '
                                     'Dont pass a file without flag to clang! Use `--dest-file=` instead.')
    parser.add_argument('--src-file', dest='srcfile', action='store',
                        type=type('string'), required=True, default=None,
                        help='file with new functions definitions')
    parser.add_argument('--dest-file', dest='destfile', action='store',
                        type=type('string'), required=True,
                        help='file with old functions definitions')
    parser.add_argument('--oldfile-delete', dest='oldfile_del', action='store_true',
                        help='use this to delete old version of destination file')
    parser.add_argument('--oldfile-keep', dest='oldfile_del', action='store_false',
                        help='use this to keep old version of destination file (default)')
    parser.set_defaults(oldfile_del=False)
    args, clangcmd = parser.parse_known_args()

    if not os.path.isfile(args.srcfile):
        parser.error(f"specified source file doesn't exist:\n{args.srcfile}\n")

    if not os.path.isfile(args.destfile):
        parser.error(f"specified destination file doesn't exist:\n{args.destfile}\n")

    clangcmd_src = clangcmd.copy()
    clangcmd_dest = clangcmd.copy()
    clangcmd_src.append(args.srcfile)
    clangcmd_dest.append(args.destfile)

    index = Index.create()
    tu_src = index.parse(None, clangcmd_src)
    if not tu_src:
        parser.error(f"clang unable to load source file:\n{args.srcfile}\n")

    tu_dest = index.parse(None, clangcmd_dest)
    if not tu_dest:
        parser.error(f"clang unable to load destination file:\n{args.destfile}\n")

    # print information about unknown files/functions/methods
    pprint(('diagnostics in SOURCE:\t'+args.srcfile, [get_diag_info(d) for d in tu_src.diagnostics]))
    pprint(('diagnostics in DESTINATION:\t'+args.destfile, [get_diag_info(d) for d in tu_dest.diagnostics]))

    method_def_nodes_src = []
    find_method_def_nodes(tu_src.cursor, method_def_nodes_src, args.srcfile)
    if not method_def_nodes_src:
        parser.error(f"unable to find any method definition in source file:\n{args.srcfile}\n" +
                      f"probably you forgot to pass `-std=c++03` (or higher) flag?\n")

    method_def_nodes_dest = []
    find_method_def_nodes(tu_dest.cursor, method_def_nodes_dest, args.destfile)
    if not method_def_nodes_dest:
        parser.error(f"unable to find any function/method definition in destination file:\n{args.destfile}" +
                      f"\nprobably you forgot to pass `-std=c++3` (or higher) flag?\n")

    # read source file
    with open(args.srcfile, mode='r') as file:
        srcdata = file.readlines()
        srcdata = [line.rstrip() for line in srcdata]

    # read destination file
    with open(args.destfile, mode='r') as file:
        destdata = file.readlines()
        destdata = [line.rstrip() for line in destdata]

    dest_lines = list(range(1, len(destdata)+1))
    for node_src in method_def_nodes_src:
        node_dest = find_method_matching_node(node_src, method_def_nodes_dest)
        if not node_dest:
            err_msg = (f"unable to find any destination function/method matching for a source function/method:\n" +
                        f"\t{node_src.semantic_parent.displayname}::{node_src.spelling}->{node_src.type.spelling}\n" +
                        f"found destination functions/methods:\n")
            for node in method_def_nodes_dest:
                err_msg += f"\t{node.semantic_parent.displayname}::{node.spelling}->{node.type.spelling}\n"
            err_msg += f"also check is it definition? static? virtual? const?\n"
            parser.error(err_msg)

        idx = dest_lines.index(node_dest.extent.start.line)
        for i in range(0, node_dest.extent.end.line - node_dest.extent.start.line + 1):
            dest_lines.remove(node_dest.extent.start.line+i)   # remove by value (not by index)
            del destdata[idx]

        for i in range(0, node_src.extent.end.line - node_src.extent.start.line + 1):
            dest_lines.insert(idx + i, None)
            destdata.insert(idx + i, srcdata[node_src.extent.start.line + i - 1])

    prepared_filename = prepare_filename(args.destfile)
    with open(prepared_filename, "w") as file:
        for line in destdata:
            file.write("%s\n" % line)

    if args.oldfile_del:
        os.remove(args.destfile)
    else:
        filename, file_extension = os.path.splitext(args.destfile)
        prepared_oldfilename = prepare_filename(filename + '_OLD' + file_extension)
        os.rename(args.destfile, prepared_oldfilename)

    os.rename(prepared_filename, args.destfile)


if __name__ == '__main__':
    main()