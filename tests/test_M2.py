import unittest

from src.calculator import Calculator
from src.errors import CalculatorError


class TestCalculator(unittest.TestCase):
    def calc(self, exp: str) -> float | int:
        calc_object = Calculator()
        return calc_object.solve(exp)

    def test_addition_1(self) -> None:
        self.assertEqual(self.calc("2+3"), 5)

    def test_addition_2(self) -> None:
        self.assertEqual(self.calc("1000000000+8123719824986"), 8124719824986)

    def test_subtraction(self) -> None:
        self.assertEqual(self.calc("10-7"), 3)

    def test_multiplication(self) -> None:
        self.assertEqual(self.calc("6*7"), 42)

    def test_division(self) -> None:
        self.assertEqual(self.calc("8/2"), 4)

    def test_parentheses_1(self) -> None:
        self.assertEqual(self.calc("2+(4-5)"), 1)

    def test_parentheses_2(self) -> None:
        self.assertEqual(self.calc("2**(100-80*1.5+10+13)"), 8)

    def test_nested_parentheses(self) -> None:
        self.assertEqual(self.calc("((2+3)*(4+1))"), 25)

    def test_incorrect_parentheses(self) -> None:
        with self.assertRaises(CalculatorError):
            self.calc("(2+3")

    def test_unary_minus(self) -> None:
        self.assertEqual(self.calc("2*-3"), -6)

    def test_unary_plus(self) -> None:
        self.assertEqual(self.calc("(+3)+2"), 5)

    def test_double_minus(self) -> None:
        self.assertEqual(self.calc("3--2"), 5)

    def test_leading_zeros(self) -> None:
        self.assertEqual(self.calc("003+04"), 7)

    def test_float_and_parentheses(self) -> None:
        self.assertEqual(self.calc("(1.5+2.5)*(2/1)"), 8)

    def test_all_operations_together(self) -> None:
        self.assertEqual(self.calc("2+3*4-5/2**2+1%3//1"), 13.75)

    def test_complex_nested_parentheses(self) -> None:
        self.assertEqual(self.calc("((1+2)*(3+4)/(5-3+1))"), 7)

    def test_plus_minus_combo(self) -> None:
        self.assertEqual(self.calc("3+-2"), 1)

    def test_power_right_associative(self) -> None:
        self.assertEqual(self.calc("2**3**2"), 512)

    def test_negative_power(self) -> None:
        self.assertEqual(self.calc("2**-2"), 0.25)

    def test_square_root_as_power(self) -> None:
        self.assertEqual(self.calc("4**.5"), 2)

    def test_integer_division(self) -> None:
        self.assertEqual(self.calc("7//2"), 3)

    def test_modulo(self) -> None:
        self.assertEqual(self.calc("7%4"), 3)

    def test_integer_division_by_zero(self) -> None:
        with self.assertRaises(CalculatorError):
            self.calc("10//0")

    def test_modulo_by_zero(self) -> None:
        with self.assertRaises(CalculatorError):
            self.calc("10%0")

    def test_invalid_float_in_integer_division(self) -> None:
        with self.assertRaises(CalculatorError):
            self.calc("5.5//2")

    def test_invalid_float_in_modulo(self) -> None:
        with self.assertRaises(CalculatorError):
            self.calc("5.5%2")

    def test_float_number(self) -> None:
        self.assertEqual(self.calc("3.5+2.5"), 6)

    def test_leading_dot_float(self) -> None:
        self.assertEqual(self.calc(".5+3"), 3.5)

    def test_expression_with_leading_dot(self) -> None:
        self.assertEqual(self.calc("3+.5"), 3.5)

    def test_division_by_zero(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            self.calc("5/0")

    def test_invalid_symbols(self) -> None:
        with self.assertRaises(CalculatorError):
            self.calc("2*&1")

    def test_incorrect_exp(self) -> None:
        with self.assertRaises(CalculatorError):
            self.calc("800plus7minus100123123+((((123)")

    def test_invalid_sequence(self) -> None:
        with self.assertWarns(UserWarning):
            self.calc("2++2")

    def test_big_input_warns(self) -> None:
        with self.assertWarns(UserWarning):
            self.calc("10**3000-300*10+100000000000000213012030")

    def test_too_large_number_warns(self) -> None:
        with self.assertWarns(UserWarning):
            self.calc("10**10000")

    def test_zero_power_zero(self) -> None:
        self.assertEqual(self.calc("0**0"), 1)

    def test_rounding(self) -> None:
        c = Calculator(numbers_after_dot=3)
        self.assertEqual(c.solve('1/3'), 0.333)
