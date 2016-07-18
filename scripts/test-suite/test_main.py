import unittest
from test_resources import TestResources
from test_screen import TestScreen

def run_all_tests():
    suite = unittest.TestSuite()
    suite.addTest(TestResources())
    suite.addTest(TestScreen())

    unittest.main(verbosity=2)

if __name__ == '__main__':
    run_all_tests()