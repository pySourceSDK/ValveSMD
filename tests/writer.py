import six
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
            original_text = str(file.read())
        original_text = "\n".join(original_text.splitlines())
        test_text = "\n".join(self.smds['phy'].smd_str().splitlines())
        self.assertEqual(test_text, original_text)

        self.smds['ref'].save(self.smd_temp)
        with open(self.smd_paths['ref'], 'r') as file:
            original_text = file.read()
        test_text = "\n".join(self.smds['ref'].smd_str().splitlines())
        self.assertEqual(original_text, test_text)

    def testRepr(self):
        self.assertTrue(isinstance(repr(self.smds['ref']), six.string_types))
