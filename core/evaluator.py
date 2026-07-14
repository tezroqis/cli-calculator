"""Вычислитель выражений в обратной польской нотации (RPN)."""

from __future__ import annotations

import math
from typing import Callable

from .operations import (
    UNARY_FUNCTIONS,
    BINARY_OPERATIONS,
    CONSTANTS,
    add,
    subtract,
    multiply,
    divide,
    power,
    modulo,
    percent,
    sqrt,
    factorial,
    sin,
    cos,
    tan,
    logarithm,
    natural_log,
    absolute,
    round_value,
)
from .tokenizer import Token, TokenType


class EvaluatorError(Exception):
    """Ошибка вычисления."""

    pass


def evaluate(rpn: list[Token]) -> float:
    """Вычисляет выражение, записанное в обратной польской нотации.

    Args:
        rpn: Список токенов в постфиксной нотации (RPN).

    Returns:
        Результат вычисления.

    Raises:
        EvaluatorError: При ошибке вычисления (нехватка операндов, и т.д.).
        ZeroDivisionError: При делении на ноль.
        ValueError: При математической ошибке.
    """
    stack: list[float] = []

    for token in rpn:
        if token.type == TokenType.NUMBER:
            stack.append(float(token.value))

        elif token.type == TokenType.CONSTANT:
            const_name = str(token.value).lower()
            if const_name in CONSTANTS:
                stack.append(CONSTANTS[const_name])
            else:
                raise EvaluatorError(f"Неизвестная константа: {const_name}")

        elif token.type == TokenType.FUNCTION:
            func_name = str(token.value)

            # Унарный минус
            if func_name == "neg":
                if not stack:
                    raise EvaluatorError("Недостаточно операндов для унарного минуса")
                stack.append(-stack.pop())
                continue

            # Постфиксный факториал
            if func_name == "!":
                if not stack:
                    raise EvaluatorError("Недостаточно операндов для факториала")
                a = stack.pop()
                stack.append(factorial(a))
                continue

            # Функции без аргументов (константы обрабатываются выше)
            # Определяем, сколько аргументов нужно функции
            arg_count = token.arg_count

            if func_name in ("round", "log"):
                # Эти функции могут принимать 1 или 2 аргумента
                if len(stack) >= 2 and arg_count >= 2:
                    b = stack.pop()
                    a = stack.pop()
                    if func_name == "round":
                        stack.append(round_value(a, int(b)))
                    else:  # log
                        stack.append(logarithm(a, b))
                elif len(stack) >= 1:
                    a = stack.pop()
                    if func_name == "round":
                        stack.append(round_value(a))
                    else:  # log
                        stack.append(logarithm(a))
                else:
                    raise EvaluatorError(f"Недостаточно операндов для функции {func_name}")
            else:
                if not stack:
                    raise EvaluatorError(f"Недостаточно операндов для функции {func_name}")

                a = stack.pop()

                if func_name == "sqrt":
                    stack.append(sqrt(a))
                elif func_name == "abs":
                    stack.append(absolute(a))
                elif func_name == "sin":
                    stack.append(sin(a))
                elif func_name == "cos":
                    stack.append(cos(a))
                elif func_name == "tan":
                    stack.append(tan(a))
                elif func_name == "ln":
                    stack.append(natural_log(a))
                elif func_name == "factorial":
                    stack.append(factorial(a))
                else:
                    raise EvaluatorError(f"Неизвестная функция: {func_name}")

        elif token.type == TokenType.OPERATOR:
            op = str(token.value)

            if len(stack) < 2:
                raise EvaluatorError(
                    f"Недостаточно операндов для оператора '{op}'"
                )

            b = stack.pop()
            a = stack.pop()

            if op == "+":
                stack.append(add(a, b))
            elif op == "-":
                stack.append(subtract(a, b))
            elif op == "*":
                stack.append(multiply(a, b))
            elif op == "/":
                stack.append(divide(a, b))
            elif op in ("^", "**"):
                stack.append(power(a, b))
            elif op == "%":
                stack.append(percent(a, b))
            elif op == "mod":
                stack.append(modulo(a, b))
            else:
                raise EvaluatorError(f"Неизвестный оператор: {op}")

    if len(stack) != 1:
        raise EvaluatorError(
            f"Некорректное выражение: в стеке осталось {len(stack)} значений"
        )

    return stack[0]


def compute(expression: str) -> float:
    """Полный цикл: токенизация → парсинг → вычисление.

    Удобная функция для вычисления выражения из строки.

    Args:
        expression: Строка математического выражения.

    Returns:
        Результат вычисления.

    Raises:
        TokenizerError: При ошибке токенизации.
        ParserError: При ошибке парсинга.
        EvaluatorError: При ошибке вычисления.
        ZeroDivisionError: При делении на ноль.
        ValueError: При математической ошибке.
    """
    from .tokenizer import Tokenizer
    from .parser import parse as parse_to_rpn

    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expression)
    rpn = parse_to_rpn(tokens)
    return evaluate(rpn)