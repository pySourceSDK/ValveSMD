import unittest
from valvesmd import *


class SmdTestCase(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        return

    def testFgd(self):
        smd = SmdParse('tests/smds/stairs001.smd')
        self.assertTrue(smd.smd_str())
