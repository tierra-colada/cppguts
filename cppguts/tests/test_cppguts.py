from pathlib import Path
import shutil
import subprocess, os, filecmp
import unittest


class test_basics(unittest.TestCase):
    this_dir = os.path.dirname(__file__)
    data_dir = os.path.join(this_dir, 'data')
    tmp_dir = os.path.join(this_dir, 'tmp')
    src = os.path.join(tmp_dir, 'src.h')
    dest = os.path.join(tmp_dir, 'dest.h')
    srcin = os.path.join(data_dir, 'src.h.in')
    destin = os.path.join(data_dir, 'dest.h.in')

    def setUp(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)
        Path(self.tmp_dir).mkdir(parents=True, exist_ok=True)
        shutil.copy(self.srcin, self.src)
        shutil.copy(self.destin, self.dest)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_basics(self):
        subprocess.run(['editcpp', '--src-file', self.src, '--dest-file', self.dest, '--oldfile-keep', '-std=c++03'])

        with open(self.dest) as f:
            with open(self.destin) as fin:
                self.assertTrue(f != fin)