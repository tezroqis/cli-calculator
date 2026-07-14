"""Тесты для вычислителя RPN и полного цикла вычислений."""

from __future__ import annotations

import math
import pytest

from core.evaluator import compute, evaluate, EvaluatorError
from core.tokenizer import Tokenizer, Token
from core.parser import parse


class TestEvaluator:
    """Тесты вычислителя (полный цикл через compute)."""

    def test_simple_addition(self) -> None:
        assert compute("2 + 3") == 5.0

    def test_simple_subtraction(self) -> None:
        assert compute("5 - 2") == 3.0

    def test_simple_multiplication(self) -> None:
        assert compute("4 * 3") == 12.0

    def test_simple_division(self) -> None:
        assert compute("6 / 3") == 2.0

    def test_operator_precedence_multiplication_first(self) -> None:
        # 2 + 3 * 4 = 2 + 12 = 14
        assert compute("2 + 3 * 4") == 14.0

    def test_operator_precedence_division_first(self) -> None:
        # 10 - 6 / 3 = 10 - 2 = 8
        assert compute("10 - 6 / 3") == 8.0

    def test_parentheses_override_precedence(self) -> None:
        # (2 + 3) * 4 = 20
        assert compute("(2 + 3) * 4") == 20.0

    def test_nested_parentheses(self) -> None:
        # 2 * (3 + (4 - 1)) = 2 * (3 + 3) = 12
        assert compute("2 * (3 + (4 - 1))") == 12.0

    def test_power(self) -> None:
        assert compute("2 ^ 3") == 8.0
        assert compute("2 ** 3") == 8.0

    def test_power_right_associative(self) -> None:
        # 2 ^ 3 ^ 2 = 2 ^ (3 ^ 2) = 2 ^ 9 = 512
        assert compute("2 ^ 3 ^ 2") == 512.0

    def test_unary_minus(self) -> None:
        assert compute("-5") == -5.0
        assert compute("3 + -2") == 1.0
        assert compute("-3 + 5") == 2.0

    def test_unary_minus_with_parentheses(self) -> None:
        assert compute("(-5)") == -5.0
        assert compute("2 * (-3)") == -6.0

    def test_sqrt(self) -> None:
        assert compute("sqrt(16)") == 4.0
        assert compute("sqrt(9)") == 3.0

    def test_sqrt_with_expression(self) -> None:
        assert compute("sqrt(9 + 16)") == 5.0

    def test_sqrt_negative_error(self) -> None:
        with pytest.raises(ValueError):
            compute("sqrt(-1)")

    def test_absolute(self) -> None:
        assert compute("abs(-5)") == 5.0
        assert compute("abs(3.14)") == 3.14

    def test_sin(self) -> None:
        assert abs(compute("sin(0)")) < 1e-15
        assert abs(compute("sin(pi / 2)") - 1.0) < 1e-15

    def test_cos(self) -> None:
        assert abs(compute("cos(0)") - 1.0) < 1e-15
        assert abs(compute("cos(pi)") + 1.0) < 1e-15

    def test_tan(self) -> None:
        assert abs(compute("tan(0)")) < 1e-15
        assert abs(compute("tan(pi / 4)") - 1.0) < 1e-15

    def test_ln(self) -> None:
        assert abs(compute("ln(e)") - 1.0) < 1e-15
        assert abs(compute("ln(1)")) < 1e-15

    def test_log(self) -> None:
        assert abs(compute("log(100)") - 2.0) < 1e-15
        assert abs(compute("log(1)")) < 1e-15

    def test_factorial(self) -> None:
        assert compute("5!") == 120.0
        assert compute("factorial(5)") == 120.0
        assert compute("0!") == 1.0

    def test_factorial_of_expression(self) -> None:
        assert compute("(2 + 1)!") == 6.0

    def test_modulo(self) -> None:
        assert compute("10 mod 3") == 1.0
        assert compute("7 mod 2") == 1.0

    def test_percent(self) -> None:
        assert compute("10 % 200") == 20.0
        assert compute("50 % 100") == 50.0

    def test_constants(self) -> None:
        result = compute("pi")
        assert abs(result - math.pi) < 1e-15
        result = compute("e")
        assert abs(result - math.e) < 1e-15

    def test_round(self) -> None:
        assert compute("round(3.7)") == 4.0
        assert compute("round(3.2)") == 3.0

    def test_division_by_zero(self) -> None:
        with pytest.raises(ZeroDivisionError):
            compute("1 / 0")

    def test_complex_expression_1(self) -> None:
        # 3 + 4 * 2 / (1 - 5) ^ 2
        # = 3 + 8 / (-4)^2 = 3 + 8 / 16 = 3 + 0.5 = 3.5
        assert compute("3 + 4 * 2 / (1 - 5) ^ 2") == 3.5

    def test_complex_expression_2(self) -> None:
        # sin(pi/2) + log(100) - sqrt(16) * 2
        # = 1 + 2 - 4 * 2 = 1 + 2 - 8 = -5
        result = compute("sin(pi / 2) + log(100) - sqrt(16) * 2")
        assert abs(result - (-5.0)) < 1e-15

    def test_float_result(self) -> None:
        assert compute("5 / 2") == 2.5

    def test_unary_plus_ignored(self) -> None:
        assert compute("+5") == 5.0
        assert compute("3 + +2") == 5.0


class TestEvaluateDirect:
    """Тесты прямого вызова evaluate() с вручную собранными RPN-токенами."""

    def test_direct_rpn_addition(self) -> None:
        rpn = [
            Token(TokenType.NUMBER, 2.0),
            Token(TokenType.NUMBER, 3.0),
            Token(TokenType.OPERATOR, "+"),
        ]
        assert evaluate(rpn) == 5.0

    def test_direct_rpn_constant(self) -> None:
        rpn = [Token(TokenType.CONSTANT, "pi")]
        assert abs(evaluate(rpn) - math.pi) < 1e-15

    def test_direct_rpn_unary_minus(self) -> None:
        rpn = [
            Token(TokenType.NUMBER, 5.0),
            Token(TokenType.FUNCTION, "neg"),
        ]
        assert evaluate(rpn) == -5.0

    def test_direct_rpn_insufficient_operands(self) -> None:
        rpn = [
            Token(TokenType.NUMBER, 2.0),
            Token(TokenType.OPERATOR, "+"),
        ]
        with pytest.raises(EvaluatorError, match="Недостаточно операндов"):
            evaluate(rpn)

    def test_direct_rpn_extra_values(self) -> None:
        rpn = [
            Token(TokenType.NUMBER, 2.0),
            Token(TokenType.NUMBER, 3.0),
            Token(TokenType.NUMBER, 4.0),
            Token(TokenType.OPERATOR, "+"),
        ]
        with pytest.raises(EvaluatorError, match="стеке осталось"):
            evaluate(rpn)

    def test_direct_rpn_unknown_function(self) -> None:
        rpn = [
            Token(TokenType.NUMBER, 1.0),
            Token(TokenType.FUNCTION, "unknown_func"),
        ]
        with pytest.raises(EvaluatorError, match="Неизвестная функция"):
            evaluate(rpn)

    def test_direct_rpn_unknown_operator(self) -> None:
        rpn = [
            Token(TokenType.NUMBER, 2.0),
            Token(TokenType.NUMBER, 3.0),
            Token(TokenType.OPERATOR, "??"),
        ]
        with pytest.raises(EvaluatorError, match="Неизвестный оператор"):
            evaluate(rpn)