import os
import tempfile
import unittest
from valvesmd import *


class SmdWriteTestCase(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.smd_file = os.path.join(self.test_dir, 'test.smd')
        self.smd = SmdParse('tests/smds/stairs001.smd')
        return

    def tearDown(self):
        return

    def testWriteSmd(self):

        SmdWrite(self.smd, self.smd_file)
        with open(self.smd_file, 'r') as file:
            text_result = file.read()

        self.assertEqual(text_result, self.smd.smd_str())

    def testWriteExact(self):
        SmdWrite(self.smd, self.smd_file)
        with open('tests/smds/stairs001.smd', 'r') as file:
            text_result = file.read()

        self.assertEqual(text_result, self.smd.smd_str())
