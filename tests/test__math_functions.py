import math_functions
import unittest

class MathFunctionsTest(unittest.TestCase):
    def test_sum(self):
        assert math_functions.sum(2, 2) == 4
        assert math_functions.sum(5, 2) == 7
        
    def test_sus(self):
        assert math_functions.sus(2, 2) == 0
        assert math_functions.sus(5, 2) == 3

    def test_times(self):
        assert math_functions.times(2, 2) == 4
        assert math_functions.times(5, 2) == 10
