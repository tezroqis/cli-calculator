"""Тесты для парсера математических выражений (shunting-yard)."""

from __future__ import annotations

import pytest

from core.tokenizer import Tokenizer, Token, TokenType, TokenizerError
from core.parser import parse, ParserError


class TestParser:
    """Тесты парсера (shunting-yard → RPN)."""

    def setup_method(self) -> None:
        self.tokenizer = Tokenizer()

    def _rpn_values(self, expression: str) -> list[object]:
        """Вспомогательный метод: токенизирует и парсит выражение,
        возвращает значения токенов в RPN."""
        tokens = self.tokenizer.tokenize(expression)
        rpn = parse(tokens)
        return [t.value for t in rpn]

    def test_simple_number(self) -> None:
        values = self._rpn_values("42")
        assert values == [42.0]

    def test_simple_addition(self) -> None:
        # 2 + 3 → RPN: 2 3 +
        values = self._rpn_values("2 + 3")
        assert values == [2.0, 3.0, "+"]

    def test_simple_subtraction(self) -> None:
        values = self._rpn_values("5 - 2")
        assert values == [5.0, 2.0, "-"]

    def test_multiplication_precedence(self) -> None:
        # 2 + 3 * 4 → RPN: 2 3 4 * + (умножение приоритетнее)
        values = self._rpn_values("2 + 3 * 4")
        assert values == [2.0, 3.0, 4.0, "*", "+"]

    def test_parentheses_precedence(self) -> None:
        # (2 + 3) * 4 → RPN: 2 3 + 4 *
        values = self._rpn_values("(2 + 3) * 4")
        assert values == [2.0, 3.0, "+", 4.0, "*"]

    def test_nested_parentheses(self) -> None:
        # 2 * (3 + (4 - 1)) → RPN: 2 3 4 1 - + *
        values = self._rpn_values("2 * (3 + (4 - 1))")
        assert values == [2.0, 3.0, 4.0, 1.0, "-", "+", "*"]

    def test_power_right_associative(self) -> None:
        # 2 ^ 3 ^ 2 → правоассоциативно: 2 ^ (3 ^ 2)
        # RPN: 2 3 2 ^ ^
        values = self._rpn_values("2 ^ 3 ^ 2")
        assert values == [2.0, 3.0, 2.0, "^", "^"]

    def test_power_double_star(self) -> None:
        values = self._rpn_values("2 ** 3")
        assert values == [2.0, 3.0, "**"]

    def test_unary_minus_at_start(self) -> None:
        # -5 → RPN: 5 neg
        values = self._rpn_values("-5")
        assert values == [5.0, "neg"]

    def test_unary_minus_in_expression(self) -> None:
        # 3 + -2 → RPN: 3 2 neg +
        values = self._rpn_values("3 + -2")
        assert values == [3.0, 2.0, "neg", "+"]

    def test_unary_minus_in_parentheses(self) -> None:
        values = self._rpn_values("(-5)")
        assert values == [5.0, "neg"]

    def test_function_sqrt(self) -> None:
        # sqrt(16) → RPN: 16 sqrt
        values = self._rpn_values("sqrt(16)")
        assert values == [16.0, "sqrt"]

    def test_function_sin(self) -> None:
        values = self._rpn_values("sin(0)")
        assert values == [0.0, "sin"]

    def test_function_with_expression(self) -> None:
        # sqrt(9 + 16) → RPN: 9 16 + sqrt
        values = self._rpn_values("sqrt(9 + 16)")
        assert values == [9.0, 16.0, "+", "sqrt"]

    def test_constant_pi(self) -> None:
        values = self._rpn_values("pi")
        assert values == ["pi"]

    def test_constant_e(self) -> None:
        values = self._rpn_values("e")
        assert values == ["e"]

    def test_constant_in_expression(self) -> None:
        values = self._rpn_values("pi / 2")
        assert values == ["pi", 2.0, "/"]

    def test_factorial_postfix(self) -> None:
        values = self._rpn_values("5!")
        assert values == [5.0, "!"]

    def test_mod_operator(self) -> None:
        values = self._rpn_values("10 mod 3")
        assert values == [10.0, 3.0, "mod"]

    def test_percent_operator(self) -> None:
        values = self._rpn_values("10 % 200")
        assert values == [10.0, 200.0, "%"]

    def test_mismatched_parens_open(self) -> None:
        with pytest.raises(ParserError, match="лишняя открывающая"):
            self._rpn_values("(2 + 3")

    def test_mismatched_parens_close(self) -> None:
        with pytest.raises(ParserError, match="лишняя закрывающая"):
            self._rpn_values("2 + 3)")

    def test_complex_expression(self) -> None:
        # 3 + 4 * 2 / (1 - 5) ^ 2
        # RPN: 3 4 2 * 1 5 - 2 ^ / +
        values = self._rpn_values("3 + 4 * 2 / (1 - 5) ^ 2")
        assert values == [3.0, 4.0, 2.0, "*", 1.0, 5.0, "-", 2.0, "^", "/", "+"]