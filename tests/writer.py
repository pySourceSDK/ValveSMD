import os
import tempfile
import unittest
from valvesmd import *


class SmdWriteTestCase(unittest.TestCase):
    def setUp(self):
        self.smd_paths = {'ref': 'tests/smds/stairs001.smd',
                          'phy': 'tests/smds/stairs001_phymodel.smd'}
        self.smds = {'ref': Smd(self.smd_paths['ref']),
                     'phy': Smd(self.smd_paths['phy'])}
        self.temp_dir = tempfile.mkdtemp()
        self.smd_temp = os.path.join(self.temp_dir, 'test.smd')
        return

    def tearDown(self):
        return

    def testWriteSmd(self):
        self.smds['ref'].save(self.smd_temp)
        with open(self.smd_temp, 'r') as file:
            text_result = file.read()
        self.assertEqual(text_result, self.smds['ref'].smd_str())

    def testWriteExact(self):
        self.smds['phy'].save(self.smd_temp)
        with open(self.smd_paths['phy'], 'r') as file:
            original_text = file.read()

        self.assertEqual(original_text, self.smds['phy'].smd_str())

        self.smds['ref'].save(self.smd_temp)
        with open(self.smd_paths['ref'], 'r') as file:
            original_text = file.read()

        self.assertEqual(original_text, self.smds['ref'].smd_str())

    def testRepr(self):
        self.assertIsInstance(repr(self.smds['ref']), str)
