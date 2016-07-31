# Some hack to get shit to work
import os, sys
_test_cwd = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.abspath(_test_cwd + "/.."))

import unittest
from test_resources import TestResources
from test_screen import TestScreen
from test_parser import TestParser
from test_timely_common import TestCommon


def run_all_tests():
    suite = unittest.TestSuite()
    suite.addTest(TestParser())
    suite.addTest(TestCommon())
    suite.addTest(TestResources())
    suite.addTest(TestScreen())

    unittest.main(verbosity=2)

if __name__ == '__main__':
    run_all_tests()
