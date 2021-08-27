import unittest
import os
import tempfile
import pyparsing
from valvesmd import *


class SmdParseTestCase(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.smd_file = os.path.join(self.test_dir, 'test.smd')

    def tearDown(self):
        return

    def testSmd(self):
        smd = Smd('tests/smds/stairs001.smd')
        self.assertEqual(len(smd.triangles), 112)

        smd = Smd('tests/smds/stairs001_phymodel.smd')
        self.assertEqual(len(smd.triangles), 24)

    def testMissingSmd(self):
        with self.assertRaises(Exception):
            smd = Smd('tests/smds/stairs002.smd')

    def testSyntaxErrorSmd(self):
        f = open(self.smd_file, "w")
        f.write("this file is obviously invalid")
        f.close()

        with self.assertRaises(pyparsing.ParseException):
            smd = Smd(self.smd_file)
