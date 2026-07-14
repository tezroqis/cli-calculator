"""Парсер математических выражений (алгоритм сортировочной станции / shunting-yard).

Преобразует последовательность токенов в обратную польскую нотацию (RPN).
Поддерживает бинарные операторы, унарные функции, скобки, константы.
"""

from __future__ import annotations

from .tokenizer import (
    ASSOCIATIVITY,
    PRECEDENCE,
    Associativity,
    Token,
    TokenType,
)


class ParserError(Exception):
    """Ошибка парсинга."""

    pass


def parse(tokens: list[Token]) -> list[Token]:
    """Преобразует список токенов в обратную польскую нотацию (RPN).

    Использует алгоритм shunting-yard Дейкстры.
    На выходе — список токенов в постфиксной нотации,
    готовый для вычисления.

    Args:
        tokens: Список токенов в инфиксной нотации.

    Returns:
        Список токенов в постфиксной нотации (RPN).

    Raises:
        ParserError: При синтаксической ошибке (несогласованные скобки и т.д.).
    """
    output: list[Token] = []
    operator_stack: list[Token] = []
    arg_count_stack: list[int] = []
    prev_token: Token | None = None

    def _is_unary_minus(idx: int) -> bool:
        """Определяет, является ли минус унарным."""
        if idx == 0:
            return True
        prev = tokens[idx - 1]
        return prev.type in (TokenType.OPERATOR, TokenType.LPAREN, TokenType.COMMA, TokenType.FUNCTION)

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Обработка унарного минуса
        if token.type == TokenType.OPERATOR and token.value == "-" and _is_unary_minus(i):
            token = Token(TokenType.FUNCTION, "neg")
        # Обработка унарного плюса (просто пропускаем)
        elif token.type == TokenType.OPERATOR and token.value == "+" and _is_unary_minus(i):
            i += 1
            continue

        if token.type == TokenType.NUMBER:
            output.append(token)

        elif token.type == TokenType.CONSTANT:
            output.append(token)

        elif token.type == TokenType.FUNCTION:
            # Функции отправляются в стек
            operator_stack.append(token)
            arg_count_stack.append(1)

        elif token.type == TokenType.OPERATOR:
            # Пока на вершине стека оператор с большим приоритетом
            # (или равным для левоассоциативных) — выталкиваем в output.
            # Унарные функции (neg, !) всегда выталкиваются перед бинарным оператором,
            # так как имеют более высокий приоритет.
            while operator_stack:
                top = operator_stack[-1]
                if top.type == TokenType.FUNCTION:
                    output.append(operator_stack.pop())
                    continue
                if top.type != TokenType.OPERATOR:
                    break
                top_prec = PRECEDENCE.get(str(top.value), 0)
                cur_prec = PRECEDENCE.get(str(token.value), 0)
                top_assoc = ASSOCIATIVITY.get(str(top.value), Associativity.LEFT)

                if (
                    (top_assoc == Associativity.LEFT and cur_prec <= top_prec)
                    or (top_assoc == Associativity.RIGHT and cur_prec < top_prec)
                ):
                    output.append(operator_stack.pop())
                else:
                    break
            operator_stack.append(token)

        elif token.type == TokenType.LPAREN:
            operator_stack.append(token)

        elif token.type == TokenType.RPAREN:
            # Выталкиваем всё до открывающей скобки
            while operator_stack and operator_stack[-1].type != TokenType.LPAREN:
                output.append(operator_stack.pop())

            if not operator_stack:
                raise ParserError("Несогласованные скобки: лишняя закрывающая скобка")

            operator_stack.pop()  # Убираем LPAREN

            # Если перед скобкой была функция — выталкиваем её
            if operator_stack and operator_stack[-1].type == TokenType.FUNCTION:
                func_token = operator_stack.pop()
                if arg_count_stack:
                    func_token.arg_count = arg_count_stack.pop()
                output.append(func_token)

        elif token.type == TokenType.COMMA:
            # Выталкиваем до открывающей скобки (разделитель аргументов)
            while operator_stack and operator_stack[-1].type != TokenType.LPAREN:
                output.append(operator_stack.pop())

            if not operator_stack:
                raise ParserError("Запятая вне вызова функции")

            # Увеличиваем счётчик аргументов для текущей функции
            # (arg_count_stack содержит счётчики только для функций, не для скобок)
            if arg_count_stack:
                arg_count_stack[-1] += 1

        prev_token = token
        i += 1

    # Выталкиваем оставшиеся операторы
    while operator_stack:
        top = operator_stack.pop()
        if top.type == TokenType.LPAREN:
            raise ParserError("Несогласованные скобки: лишняя открывающая скобка")
        output.append(top)

    return output