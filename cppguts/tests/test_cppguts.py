import unittest, pathlib


class test_basics(unittest.TestCase):
    def setUp(self):
        self.srcin = 'data/src.h.in'
        self.destin = 'data/dest.h.in'
        self.src = 'data/tmp/src.h'
        self.dest = 'data/tmp/dest.h'

    def tearDown(self):
        h5File = self.seisContainer.getH5File()

    seisContainer = None
    p = h5geo.SeisParam()
    FILE_NAME = None
    SEIS_NAME1 = None
    SEIS_NAME2 = None

    def test_createContainer(self):
        self.assertTrue(os.path.isfile(self.FILE_NAME))

    def test_createSeisWithDifferentCreateFlags(self):
        seis = self.seisContainer.createSeis(self.SEIS_NAME1, self.p, h5geo.CreationType.OPEN_OR_CREATE)
        self.assertFalse(seis is None)

        seis = self.seisContainer.createSeis(self.SEIS_NAME1, self.p, h5geo.CreationType.CREATE_OR_OVERWRITE)
        self.assertFalse(seis is None)

        seis = self.seisContainer.createSeis(self.SEIS_NAME1, self.p, h5geo.CreationType.CREATE_UNDER_NEW_NAME)
        self.assertFalse(seis is None)

        seis = self.seisContainer.createSeis(self.SEIS_NAME1, self.p, h5geo.CreationType.OPEN_OR_CREATE)
        self.assertFalse(seis is None)