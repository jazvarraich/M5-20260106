import unittest
from calculator import Calculator

class TestOperations(unittest.TestCase):

    def setUp(self):
        self.calc = Calculator(8,2)

    def test_sum(self):
        answer = self.calc.get_sum()
        self.assertEqual(answer, 10, "The answer was not 10.")


    def test_differnce(self):
        answer = self.calc.get_difference()
        self.assertEqual(answer, 6, "The answer was not 6.")

if __name__ == "__main__":
    unittest.main()