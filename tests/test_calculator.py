import unittest

from dfm18 import calculator


class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(calculator.add(3, 2), 5)
        self.assertEqual(calculator.add(5, 5), 10)
        self.assertEqual(calculator.add(7, 3), 10)
        self.assertEqual(calculator.add(1, 0), 1)

    def test_add_with_negative_numbers(self):
        self.assertEqual(calculator.add(3, -3), 0)
        self.assertEqual(calculator.add(-4, 2), -2)
        self.assertEqual(calculator.add(-15, -10), -25)

    def test_subtract(self):
        self.assertEqual(calculator.subtract(3, 2), 1)
        self.assertEqual(calculator.subtract(10, 5), 5)
        self.assertEqual(calculator.subtract(6, 3), 3)
        self.assertEqual(calculator.subtract(1, 0), 1)

    def test_subtract_with_negative_numbers(self):
        self.assertEqual(calculator.subtract(-3, 5), -8)
        self.assertEqual(calculator.subtract(10, -5), 15)
        self.assertEqual(calculator.subtract(-3, -3), 0)

    def test_multiply(self):
        self.assertEqual(calculator.multiply(3, 3), 9)
        self.assertEqual(calculator.multiply(6, 4), 24)
        self.assertEqual(calculator.multiply(9, 6), 54)
        self.assertEqual(calculator.multiply(2, 3), 6)

    def test_multiply_with_negative_numbers(self):
        self.assertEqual(calculator.multiply(3, -3), -9)
        self.assertEqual(calculator.multiply(-6, -4), 24)
        self.assertEqual(calculator.multiply(-9, 6), -54)
        self.assertEqual(calculator.multiply(-2, -3), 6)

    def test_divide(self):
        self.assertEqual(calculator.divide(3, 3), 1)
        self.assertEqual(calculator.divide(45, 9), 5)
        self.assertEqual(calculator.divide(20, 5), 4)
        self.assertEqual(calculator.divide(32, 8), 4)
        with self.assertRaises(ZeroDivisionError):
            _ = calculator.divide(1, 0)
