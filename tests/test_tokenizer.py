"""Тесты для токенизатора математических выражений."""

from __future__ import annotations

import pytest

from core.tokenizer import (
    Tokenizer,
    TokenizerError,
    Token,
    TokenType,
)


class TestTokenizer:
    """Тесты токенизатора."""

    def setup_method(self) -> None:
        self.tokenizer = Tokenizer()

    def _get_token_types(self, tokens: list[Token]) -> list[TokenType]:
        return [t.type for t in tokens]

    def _get_token_values(self, tokens: list[Token]) -> list[object]:
        return [t.value for t in tokens]

    def test_simple_number(self) -> None:
        tokens = self.tokenizer.tokenize("42")
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == 42.0

    def test_float_number(self) -> None:
        tokens = self.tokenizer.tokenize("3.14")
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == 3.14

    def test_number_starting_with_dot(self) -> None:
        tokens = self.tokenizer.tokenize(".5")
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == 0.5

    def test_double_dot_error(self) -> None:
        with pytest.raises(TokenizerError, match="Лишняя десятичная точка"):
            self.tokenizer.tokenize("1.2.3")

    def test_simple_expression(self) -> None:
        tokens = self.tokenizer.tokenize("2 + 3")
        types = self._get_token_types(tokens)
        assert types == [TokenType.NUMBER, TokenType.OPERATOR, TokenType.NUMBER]
        assert self._get_token_values(tokens) == [2.0, "+", 3.0]

    def test_all_operators(self) -> None:
        tokens = self.tokenizer.tokenize("+ - * / ^ %")
        values = self._get_token_values(tokens)
        assert values == ["+", "-", "*", "/", "^", "%"]

    def test_power_operator(self) -> None:
        tokens = self.tokenizer.tokenize("2 ** 3")
        values = self._get_token_values(tokens)
        assert values == [2.0, "**", 3.0]

    def test_parentheses(self) -> None:
        tokens = self.tokenizer.tokenize("(2 + 3) * 4")
        types = self._get_token_types(tokens)
        assert TokenType.LPAREN in types
        assert TokenType.RPAREN in types

    def test_function(self) -> None:
        tokens = self.tokenizer.tokenize("sqrt(16)")
        types = self._get_token_types(tokens)
        assert types == [
            TokenType.FUNCTION, TokenType.LPAREN,
            TokenType.NUMBER, TokenType.RPAREN,
        ]
        assert tokens[0].value == "sqrt"

    def test_constant_pi(self) -> None:
        tokens = self.tokenizer.tokenize("pi")
        assert tokens[0].type == TokenType.CONSTANT
        assert tokens[0].value == "pi"

    def test_constant_e(self) -> None:
        tokens = self.tokenizer.tokenize("e")
        assert tokens[0].type == TokenType.CONSTANT
        assert tokens[0].value == "e"

    def test_unknown_identifier(self) -> None:
        with pytest.raises(TokenizerError, match="Неизвестный идентификатор"):
            self.tokenizer.tokenize("foo")

    def test_mod_operator(self) -> None:
        tokens = self.tokenizer.tokenize("7 mod 3")
        values = self._get_token_values(tokens)
        assert values == [7.0, "mod", 3.0]

    def test_comma(self) -> None:
        tokens = self.tokenizer.tokenize("log(10, 2)")
        types = self._get_token_types(tokens)
        assert TokenType.COMMA in types

    def test_factorial_postfix(self) -> None:
        tokens = self.tokenizer.tokenize("5!")
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[1].type == TokenType.FUNCTION
        assert tokens[1].value == "!"

    def test_complex_expression(self) -> None:
        tokens = self.tokenizer.tokenize("sin(pi / 2) + 3 * (4 - 1)!")
        types = self._get_token_types(tokens)
        # sin ( pi / 2 ) + 3 * ( 4 - 1 ) !
        expected = [
            TokenType.FUNCTION, TokenType.LPAREN,
            TokenType.CONSTANT, TokenType.OPERATOR,
            TokenType.NUMBER, TokenType.RPAREN,
            TokenType.OPERATOR, TokenType.NUMBER,
            TokenType.OPERATOR, TokenType.LPAREN,
            TokenType.NUMBER, TokenType.OPERATOR,
            TokenType.NUMBER, TokenType.RPAREN,
            TokenType.FUNCTION,
        ]
        assert types == expected

    def test_negative_number_at_start(self) -> None:
        tokens = self.tokenizer.tokenize("-5")
        values = self._get_token_values(tokens)
        assert values == ["-", 5.0]

    def test_negative_number_in_parentheses(self) -> None:
        tokens = self.tokenizer.tokenize("(-5)")
        values = self._get_token_values(tokens)
        assert values == ["(", "-", 5.0, ")"]

    def test_ignore_spaces(self) -> None:
        tokens = self.tokenizer.tokenize("  2   +   3  ")
        values = self._get_token_values(tokens)
        assert values == [2.0, "+", 3.0]

    def test_unknown_symbol(self) -> None:
        with pytest.raises(TokenizerError, match="Неизвестный символ"):
            self.tokenizer.tokenize("2 $ 3")