import unittest

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
