"""
Dont test set_profile

_get_severity()
User.keywords: extracted by the parser. A param in user_profile
Keywords: List of symptoms/conditions. Each associated with rating

If user_profile in get_severity is blank, then the function should return -1

_init_disorder_severities()
Double table computations, need to ensure the final table is correct.
If one table is empty or if none match, then return default value

_disorder_confidence()
returns tuple of (name, percentage)

_calculate_adjustment()
Assume confidence_weight_factor is always 1.0
"""

import unittest
import screen
import timely_classes


class TestScreen(unittest.TestCase):

    def setUp(self):
        self.disorder_list = []
        self.test_user_profile1 = timely_classes.UserProfile()
        self.test_user_profile2 = timely_classes.UserProfile()

    # Test _calculate_adjustment() function
    def test_calculate_adjustment_failure_invalid_input_type(self):
        self.assertRaises(TypeError, screen._calculate_adjustment, "1", [2], {"Three": 4})

    def test_calculate_adjustment_success_adjust_up(self):
        self.assertEqual(screen._calculate_adjustment(0.5, 0.7, 0.3), 0.65)

    def test_calculate_adjustment_success_adjust_down(self):
        self.assertEqual(screen._calculate_adjustment(0.5, 0.2, 0.2), 0.4)

    # Test _disorder_confidence function
    def test_disorder_confidence_failure_invalid_input_type1(self):
        self.assertRaises(TypeError, screen._disorder_confidence, "1", self.disorder_list)

    def test_disorder_confidence_failure_invalid_input_type2(self):
        self.assertRaises(TypeError, screen._disorder_confidence, self.test_user_profile1, "1")

    def test_disorder_confidence_success_1(self):
        pass

    def test_disorder_confidence_success_2(self):
        pass

    # Test _init_disorder_severities() function
    def test_init_disorder_severities_failure_invalid_input_type1(self):
        self.assertRaises(TypeError, screen._init_disorder_severities, "1", [])

    def test_init_disorder_severities_failure_invalid_input_type2(self):
        self.assertRaises(TypeError, screen._init_disorder_severities, {}, 2)

    # Test _get_severity() function
    def test_get_severity_failure_invalid_input_type1(self):
        self.assertRaises(TypeError, screen._get_severity, self.test_user_profile1, "1")

    def test_get_severity_failure_invalid_input_type2(self):
        self.assertRaises(TypeError, screen._get_severity, 0, [1, 2, 3])

    def tearDown(self):
        pass
