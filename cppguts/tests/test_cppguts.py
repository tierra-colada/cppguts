from pathlib import Path
import shutil
import subprocess, os, filecmp
import unittest


class test_basics(unittest.TestCase):
    this_dir = os.path.dirname(__file__)
    data_dir = this_dir + '/data'
    tmp_dir = data_dir + '/tmp'
    src = tmp_dir + '/src.h'
    dest = tmp_dir + '/dest.h'
    srcin = data_dir + '/src.h.in'
    destin = data_dir + '/dest.h.in'

    def setUp(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)
        Path(self.tmp_dir).mkdir(parents=True, exist_ok=True)
        shutil.copy(self.srcin, self.src)
        shutil.copy(self.destin, self.dest)

    # def tearDown(self):
    #     shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_basics(self):
        subprocess.run(['editcpp', '--src-file', self.src, '--dest-file', self.dest, '--oldfile-keep', '-std=c++03'])

        with open(self.dest) as f:
            with open(self.destin) as fin:
                self.assertTrue(f != fin)