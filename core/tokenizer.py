"""Лексический анализатор (токенизатор) для математических выражений."""

from __future__ import annotations

from enum import Enum, auto
from typing import ClassVar


class TokenType(Enum):
    """Типы токенов."""

    NUMBER = auto()      # Число (целое или с плавающей точкой)
    OPERATOR = auto()    # Бинарный оператор: +, -, *, /, ^, **, mod
    LPAREN = auto()      # Открывающая скобка (
    RPAREN = auto()      # Закрывающая скобка )
    FUNCTION = auto()    # Унарная функция: sin, cos, sqrt, ln и т.д.
    CONSTANT = auto()    # Константа: pi, e
    COMMA = auto()       # Запятая (разделитель аргументов)


class Associativity(Enum):
    """Ассоциативность оператора."""

    LEFT = auto()
    RIGHT = auto()


class Token:
    """Токен математического выражения."""

    __slots__ = ("type", "value")

    def __init__(self, type: TokenType, value: float | str) -> None:
        self.type: TokenType = type
        self.value: float | str = value

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Token):
            return NotImplemented
        return self.type == other.type and self.value == other.value


# Приоритеты операторов (чем выше число, тем выше приоритет)
PRECEDENCE: dict[str, int] = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "mod": 2,
    "^": 3,
    "**": 3,
    "%": 2,
}

# Ассоциативность операторов
ASSOCIATIVITY: dict[str, Associativity] = {
    "+": Associativity.LEFT,
    "-": Associativity.LEFT,
    "*": Associativity.LEFT,
    "/": Associativity.LEFT,
    "mod": Associativity.LEFT,
    "^": Associativity.RIGHT,
    "**": Associativity.RIGHT,
    "%": Associativity.LEFT,
}

# Множество известных функций
KNOWN_FUNCTIONS: set[str] = {
    "sqrt", "abs", "sin", "cos", "tan",
    "log", "ln", "round", "factorial",
}

# Множество известных констант
KNOWN_CONSTANTS: set[str] = {"pi", "e"}


class TokenizerError(Exception):
    """Ошибка токенизации."""

    pass


class Tokenizer:
    """Лексический анализатор математических выражений.

    Разбивает входную строку на последовательность токенов.
    Поддерживает числа, операторы, скобки, функции и константы.
    """

    def __init__(self) -> None:
        self._tokens: list[Token] = []
        self._pos: int = 0

    def tokenize(self, expression: str) -> list[Token]:
        """Преобразует строку выражения в список токенов.

        Args:
            expression: Строка математического выражения.

        Returns:
            Список токенов.

        Raises:
            TokenizerError: Если встречен неизвестный символ.
        """
        self._tokens = []
        self._pos = 0
        expression = expression.strip()

        while self._pos < len(expression):
            char = expression[self._pos]

            # Пропуск пробелов
            if char.isspace():
                self._pos += 1
                continue

            # Числа (целые и с плавающей точкой)
            if char.isdigit() or (char == "." and self._peek_digit(expression)):
                self._tokenize_number(expression)
                continue

            # Идентификаторы (функции и константы)
            if char.isalpha() or char == "_":
                self._tokenize_identifier(expression)
                continue

            # Постфиксный факториал
            if char == "!":
                self._tokens.append(Token(TokenType.FUNCTION, "!"))
                self._pos += 1
                continue

            # Операторы и скобки
            if char in "+-*/^()%,=<>":
                self._tokenize_operator_or_paren(expression)
                continue

            raise TokenizerError(
                f"Неизвестный символ '{char}' на позиции {self._pos}"
            )

        return self._tokens

    def _tokenize_number(self, expression: str) -> None:
        """Извлекает числовой токен."""
        start = self._pos
        dots = 0
        while self._pos < len(expression) and (
            expression[self._pos].isdigit() or expression[self._pos] == "."
        ):
            if expression[self._pos] == ".":
                dots += 1
                if dots > 1:
                    raise TokenizerError(
                        f"Лишняя десятичная точка в числе на позиции {self._pos}"
                    )
            self._pos += 1

        num_str = expression[start : self._pos]
        self._tokens.append(Token(TokenType.NUMBER, float(num_str)))

    def _tokenize_identifier(self, expression: str) -> None:
        """Извлекает идентификатор (функцию или константу)."""
        start = self._pos
        while self._pos < len(expression) and (
            expression[self._pos].isalnum() or expression[self._pos] == "_"
        ):
            self._pos += 1

        ident = expression[start : self._pos].lower()

        if ident in KNOWN_CONSTANTS:
            self._tokens.append(Token(TokenType.CONSTANT, ident))
        elif ident in KNOWN_FUNCTIONS:
            self._tokens.append(Token(TokenType.FUNCTION, ident))
        elif ident == "mod":
            self._tokens.append(Token(TokenType.OPERATOR, "mod"))
        else:
            raise TokenizerError(
                f"Неизвестный идентификатор '{ident}' на позиции {start}"
            )

    def _tokenize_operator_or_paren(self, expression: str) -> None:
        """Извлекает оператор, скобку или запятую."""
        char = expression[self._pos]

        # Двухсимвольный оператор **
        if char == "*" and self._pos + 1 < len(expression) and expression[self._pos + 1] == "*":
            self._tokens.append(Token(TokenType.OPERATOR, "**"))
            self._pos += 2
            return

        # Скобки
        if char == "(":
            self._tokens.append(Token(TokenType.LPAREN, "("))
            self._pos += 1
            return
        if char == ")":
            self._tokens.append(Token(TokenType.RPAREN, ")"))
            self._pos += 1
            return

        # Запятая
        if char == ",":
            self._tokens.append(Token(TokenType.COMMA, ","))
            self._pos += 1
            return

        # Обычные операторы
        if char in "+-*/^%":
            self._tokens.append(Token(TokenType.OPERATOR, char))
            self._pos += 1
            return

        raise TokenizerError(
            f"Неизвестный символ '{char}' на позиции {self._pos}"
        )

    def _peek_digit(self, expression: str) -> bool:
        """Проверяет, следует ли цифра после текущей позиции."""
        next_pos = self._pos + 1
        return next_pos < len(expression) and expression[next_pos].isdigit()