import os
import unittest
import tempfile
from valvesmd import *
from valvesmd.utils import *
from valvesmd.utils import _cardinal


class SmdUtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.smd_file = os.path.join(self.test_dir, 'test.smd')
        self.smd = SmdParse('tests/smds/stairs001.smd')
        return

    def tearDown(self):
        return

    def testCardinalSmd(self):
        self.assertEqual(_cardinal(-4.5), -1)
        self.assertEqual(_cardinal(5), 1)
        self.assertEqual(_cardinal(0), 0)

    def testMirrorSmd(self):
        mirrorSmd(self.smd, 'x')
        mirrorSmd(self.smd, 'y')
        mirrorSmd(self.smd, 'z')
        with self.assertRaises(ValueError):
            mirrorSmd(self.smd, 'u')

    def testScaleSmd(self):
        scaleSmd(self.smd)
        scaleSmd(self.smd, 2)
        scaleSmd(self.smd, 0.5)
        scaleSmd(self.smd, (0.5, 2, 1))
        with self.assertRaises(ValueError):
            scaleSmd(self.smd, None)

    def testTranslateSmd(self):
        translateSmd(self.smd)
        self.assertTrue(True)

    def testCleanSmd(self):
        self.assertEqual(len(self.smd.triangles), 112)
        cleanSmd(self.smd)
        self.assertEqual(len(self.smd.triangles), 108)

    def testmatReplaceSmd(self):
        matReplaceSmd(self.smd, 'TOOLSNODRAW', 'WOOD_BRIDGE001')
        for triangle in self.smd.triangles:
            self.assertNotEqual(triangle.material, 'TOOLSNODRAW')
