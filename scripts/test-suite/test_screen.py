"""
Dont test set_profile

_get_severity()
User.keywords: extracted by the parser. A param in user_profile
Keywords: List of symptoms/conditions. Each associated with rating

If user_profile in get_severity is blank, then the function should return -1

__init_disorder_severity()
Double table computations, need to ensure the final table is correct.
If one table is empty or if none match, then return default value

_disorder_confidence()
returns tuple of (name, percentage)

_calculate_adjustment()
Assume confidence_weight_factor is always 1.0
"""

# Some hack to get shit to work
import os, sys
sys.path.insert(0, os.path.abspath(".."))
import unittest
import screen

class TestScreen(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        pass

    def test_failure(self):
        self.assertEqual(1, 0)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
