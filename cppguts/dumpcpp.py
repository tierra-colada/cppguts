from clang.cindex import Index
from clang.cindex import Cursor
from pprint import pprint
import argparse, os


def get_diag_info(diag):
    return {'severity': diag.severity,
            'location': diag.location,
            'category_name': diag.category_name,
            'spelling': diag.spelling,
            'ranges': diag.ranges,
            'fixits': diag.fixits}


def get_node_info(node: Cursor, children = None) -> dict:
    return {'access_specifier': node.access_specifier,
            'availability': node.availability,
            'brief_comment': node.brief_comment,
            'canonical': node.canonical,
            'data': node.data,
            'displayname': node.displayname,
            # 'enum_type' : node.enum_type,
            # 'enum_value' : node.enum_value,
            'exception_specification_kind': node.exception_specification_kind,
            'extent': node.extent,
            'from_cursor_result': node.from_cursor_result,
            'from_location': node.from_location,
            'from_result': node.from_result,
            'get_arguments': node.get_arguments(),
            'get_bitfield_width': node.get_bitfield_width(),
            'get_children': node.get_children(),
            'get_definition': node.get_definition(),
            'get_field_offsetof': node.get_field_offsetof(),
            # 'get_included_file' : node.get_included_file(),
            'get_num_template_arguments': node.get_num_template_arguments(),
            # 'get_template_argument_kind' : node.get_template_argument_kind(),
            # 'get_template_argument_type' : node.get_template_argument_type(),
            # 'get_template_argument_unsigned_value' : node.get_template_argument_unsigned_value(),
            # 'get_template_argument_value' : node.get_template_argument_value(),
            'get_tokens': node.get_tokens(),
            'get_usr': node.get_usr(),
            'hash': node.hash,
            'is_abstract_record': node.is_abstract_record(),
            'is_anonymous': node.is_anonymous(),
            'is_bitfield': node.is_bitfield(),
            'is_const_method': node.is_const_method(),
            'is_converting_constructor': node.is_converting_constructor(),
            'is_copy_constructor': node.is_copy_constructor(),
            'is_default_constructor': node.is_default_constructor(),
            'is_default_method': node.is_default_method(),
            'is_definition': node.is_definition(),
            'is_move_constructor': node.is_move_constructor(),
            'is_mutable_field': node.is_mutable_field(),
            'is_pure_virtual_method': node.is_pure_virtual_method(),
            'is_scoped_enum': node.is_scoped_enum(),
            'is_static_method': node.is_static_method(),
            'is_virtual_method': node.is_virtual_method(),
            'kind': node.kind,
            'lexical_parent.displayname': node.lexical_parent.displayname if node.lexical_parent else None,
            'linkage': node.linkage,
            'location': node.location,
            # 'mangled_name': node.mangled_name if node.mangled_name else None,
            # 'objc_type_encoding': node.objc_type_encoding,
            # 'raw_comment': node.raw_comment,
            # 'referenced': node.referenced,
            'result_type spelling': node.result_type.spelling,
            'semantic_parent.displayname': node.semantic_parent.displayname if node.semantic_parent else None,
            'spelling': node.spelling,
            'storage_class': node.storage_class,
            # 'tls_kind': node.tls_kind,
            'translation_unit spelling': node.translation_unit.spelling if node.translation_unit else None,
            'type spelling': node.type.spelling,
            # 'underlying_typedef_type spelling': node.underlying_typedef_type.spelling if node.underlying_typedef_type else None,
            # 'walk_preorder': node.walk_preorder,
            # 'xdata': node.xdata,
            'children' : children}


def find_nodes(node: Cursor, nodes_found: list, objname: str):
    if objname and objname == node.spelling:
        nodes_found.append(node)

    for child in node.get_children():
        find_nodes(child, nodes_found, objname)


def get_info(node: Cursor, maxdepth: int = None, depth: int = 0) -> dict:
    if maxdepth is not None and depth >= maxdepth:
        children = None
    else:
        children = [get_info(c, maxdepth, depth+1)
                    for c in node.get_children()]

    return get_node_info(node, children)


def main():
    parser = argparse.ArgumentParser(description=
                                     'Dump C++ file or dump only specified names.'
                                     'After passing `correctcpp` flags you are allowed to pass clang '
                                     'commands like `-I` (to include dir), `-std=c++17` and other. '
                                     'Dont pass a file without flag to clang! Use `--dest-file=` instead.')
    parser.add_argument('--file', dest='file', action='store',
                        type=type('string'), required=True, default=None,
                        help='file to be dumped')
    parser.add_argument("--max-depth", dest="maxdepth", action='store',
                        metavar="N", type=int, required=False, default=None,
                        help="limit cursor expansion to depth N",)
    parser.add_argument("--object-name", dest="objname", action='store',
                        type=type('string'), required=False, default=None,
                        help="parse only specified names (spelling)")
    args, clangcmd = parser.parse_known_args()

    if not os.path.isfile(args.file):
        parser.error(f"specified file doesn't exist:\n{args.file}")

    clangcmd.append(args.file)

    index = Index.create()
    tu = index.parse(None, clangcmd)
    if not tu:
        parser.error("unable to load input")

    pprint(('diagnostics:', [get_diag_info(d) for d in tu.diagnostics]))
    if args.objname:
        nodes_found = []
        find_nodes(tu.cursor, nodes_found, args.objname)
        for node in nodes_found:
            pprint(('found node', get_node_info(node)), indent=10)
    else:
        pprint(('nodes', get_info(tu.cursor)))


if __name__ == '__main__':
    main()