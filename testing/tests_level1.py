import unittest
from calculator import Calculator

class TestOperations(unittest.TestCase):

    def test_sum(self):
        calc = Calculator(8,2)
        answer = calc.get_sum()
        print(f'The answer was {answer}. \n Test Results:')
        self.assertEqual(answer, 10, "The answer was not 10.")


    def test_differnce(self):
        calc = Calculator(8,2)
        answer = calc.get_difference()
        print(f'The answer was {answer}. \n Test Results:')
        self.assertEqual(answer, 6, "The answer was not 6.")

if __name__ == "__main__":
    unittest.main()