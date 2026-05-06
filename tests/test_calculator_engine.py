import unittest

from calculator import CalculatorEngine


class TestCalculatorEngine(unittest.TestCase):
    def setUp(self):
        self.calc = CalculatorEngine()

    def display(self):
        return self.calc.get_display()

    def test_addition(self):
        self.calc.press_digit('1')
        self.calc.press_digit('2')
        self.calc.press_operator('+')
        self.calc.press_digit('3')
        self.calc.press_equals()
        self.assertEqual(self.display(), '15')

    def test_subtraction(self):
        self.calc.press_digit('5')
        self.calc.press_operator('-')
        self.calc.press_digit('8')
        self.calc.press_equals()
        self.assertEqual(self.display(), '-3')

    def test_multiplication(self):
        self.calc.press_digit('7')
        self.calc.press_operator('*')
        self.calc.press_digit('6')
        self.calc.press_equals()
        self.assertEqual(self.display(), '42')

    def test_division(self):
        self.calc.press_digit('7')
        self.calc.press_operator('/')
        self.calc.press_digit('2')
        self.calc.press_equals()
        self.assertEqual(self.display(), '3.5')

    def test_division_by_zero(self):
        self.calc.press_digit('5')
        self.calc.press_operator('/')
        self.calc.press_digit('0')
        self.calc.press_equals()
        self.assertIn('Fehler', self.display())
        self.assertIn('Division durch 0', self.display())
        # Reset
        self.calc.press_clear()
        self.assertEqual(self.display(), '0')
        # After reset, should work again
        self.calc.press_digit('2')
        self.calc.press_operator('+')
        self.calc.press_digit('2')
        self.calc.press_equals()
        self.assertEqual(self.display(), '4')

    def test_multi_digit_and_decimal(self):
        self.calc.press_digit('1')
        self.calc.press_digit('2')
        self.calc.press_dot()
        self.calc.press_digit('3')
        self.calc.press_digit('4')
        self.calc.press_operator('+')
        self.calc.press_digit('0')
        self.calc.press_dot()
        self.calc.press_digit('6')
        self.calc.press_digit('6')
        self.calc.press_equals()
        # 12.34 + 0.66 = 13.0, displayed as 13
        self.assertEqual(self.display(), '13')

    def test_operator_change_before_second_operand(self):
        self.calc.press_digit('5')
        self.calc.press_operator('+')
        # Change mind: use * instead
        self.calc.press_operator('*')
        self.calc.press_digit('2')
        self.calc.press_equals()
        self.assertEqual(self.display(), '10')

    def test_chained_operations_left_associative(self):
        # (2 + 3) * 4 = 20 with immediate execution
        self.calc.press_digit('2')
        self.calc.press_operator('+')
        self.calc.press_digit('3')
        self.calc.press_operator('*')  # triggers 2+3
        self.calc.press_digit('4')
        self.calc.press_equals()
        self.assertEqual(self.display(), '20')

    def test_equals_without_operator(self):
        self.calc.press_digit('4')
        self.calc.press_digit('2')
        self.calc.press_equals()
        self.assertEqual(self.display(), '42')

    def test_leading_dot_becomes_zero_point(self):
        self.calc.press_dot()
        self.calc.press_digit('5')
        self.calc.press_equals()
        self.assertEqual(self.display(), '0.5')

    def test_multiple_dots_prevented(self):
        self.calc.press_digit('1')
        self.calc.press_dot()
        self.calc.press_digit('2')
        # second dot should be ignored
        self.calc.press_dot()
        self.calc.press_digit('3')
        self.calc.press_equals()
        self.assertEqual(self.display(), '1.23')

    def test_clear(self):
        self.calc.press_digit('9')
        self.calc.press_operator('-')
        self.calc.press_digit('1')
        self.calc.press_clear()
        self.assertEqual(self.display(), '0')


if __name__ == '__main__':
    unittest.main()
