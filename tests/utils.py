import os
import unittest
import tempfile
from valvesmd import *
from valvesmd.utils import *


class SmdUtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.smd_file = os.path.join(self.test_dir, 'test.smd')
        self.smd = Smd('tests/smds/stairs001.smd')
        return

    def tearDown(self):
        return

    def testMirrorSmd(self):
        SmdMirror(self.smd, 'x')
        SmdMirror(self.smd, 'y')
        SmdMirror(self.smd, 'z')
        with self.assertRaises(ValueError):
            SmdMirror(self.smd, 'u')

    def testScaleSmd(self):
        SmdScale(self.smd)
        SmdScale(self.smd, 2)
        SmdScale(self.smd, 0.5)
        SmdScale(self.smd, (0.5, 2, 1))

        with self.assertRaises(ValueError):
            SmdScale(self.smd, None)

    def testTranslateSmd(self):
        SmdTranslate(self.smd)
        self.assertTrue(True)

        with self.assertRaises(ValueError):
            SmdTranslate(self.smd, None)

    def testCleanSmd(self):
        SmdClean(self.smd)
        self.assertEqual(len(self.smd.triangles), 108)

    def testmatReplaceSmd(self):
        SmdMatReplace(self.smd, 'TOOLSNODRAW', 'WOOD_BRIDGE001')
        for triangle in self.smd.triangles:
            self.assertNotEqual(triangle.material, 'TOOLSNODRAW')
