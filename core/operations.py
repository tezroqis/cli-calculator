"""Модуль математических операций калькулятора."""

from __future__ import annotations

import math
from typing import Callable


def add(a: float, b: float) -> float:
    """Сложение двух чисел.

    Args:
        a: Первое слагаемое.
        b: Второе слагаемое.

    Returns:
        Сумма a и b.
    """
    return a + b


def subtract(a: float, b: float) -> float:
    """Вычитание двух чисел.

    Args:
        a: Уменьшаемое.
        b: Вычитаемое.

    Returns:
        Разность a и b.
    """
    return a - b


def multiply(a: float, b: float) -> float:
    """Умножение двух чисел.

    Args:
        a: Первый множитель.
        b: Второй множитель.

    Returns:
        Произведение a и b.
    """
    return a * b


def divide(a: float, b: float) -> float:
    """Деление двух чисел.

    Args:
        a: Делимое.
        b: Делитель.

    Returns:
        Частное a / b.

    Raises:
        ZeroDivisionError: Если делитель равен нулю.
    """
    if b == 0:
        raise ZeroDivisionError("Деление на ноль невозможно.")
    return a / b


def power(a: float, b: float) -> float:
    """Возведение числа a в степень b.

    Args:
        a: Основание.
        b: Показатель степени.

    Returns:
        a в степени b.
    """
    return a ** b


def sqrt(a: float) -> float:
    """Квадратный корень числа.

    Args:
        a: Подкоренное выражение.

    Returns:
        Квадратный корень из a.

    Raises:
        ValueError: Если a отрицательное.
    """
    if a < 0:
        raise ValueError("Квадратный корень из отрицательного числа невозможен.")
    return math.sqrt(a)


def factorial(a: float) -> float:
    """Факториал целого неотрицательного числа.

    Args:
        a: Число для вычисления факториала.

    Returns:
        Факториал a (a!).

    Raises:
        ValueError: Если a отрицательное или не целое.
    """
    if a < 0:
        raise ValueError("Факториал отрицательного числа не определён.")
    if not a.is_integer():
        raise ValueError("Факториал определён только для целых чисел.")
    return float(math.factorial(int(a)))


def modulo(a: float, b: float) -> float:
    """Остаток от деления a на b.

    Args:
        a: Делимое.
        b: Делитель.

    Returns:
        Остаток от деления a % b.

    Raises:
        ZeroDivisionError: Если делитель равен нулю.
    """
    if b == 0:
        raise ZeroDivisionError("Деление на ноль невозможно.")
    return a % b


def percent(a: float, b: float) -> float:
    """Процент: a процентов от числа b.

    Args:
        a: Процент.
        b: Базовое число.

    Returns:
        a процентов от b.
    """
    return (a / 100) * b


def sin(a: float, radians: bool = True) -> float:
    """Синус угла.

    Args:
        a: Угол.
        radians: Если True — угол в радианах, иначе в градусах.

    Returns:
        Синус угла a.
    """
    if not radians:
        a = math.radians(a)
    return math.sin(a)


def cos(a: float, radians: bool = True) -> float:
    """Косинус угла.

    Args:
        a: Угол.
        radians: Если True — угол в радианах, иначе в градусах.

    Returns:
        Косинус угла a.
    """
    if not radians:
        a = math.radians(a)
    return math.cos(a)


def tan(a: float, radians: bool = True) -> float:
    """Тангенс угла.

    Args:
        a: Угол.
        radians: Если True — угол в радианах, иначе в градусах.

    Returns:
        Тангенс угла a.

    Raises:
        ValueError: Если тангенс не определён (cos = 0).
    """
    if not radians:
        a = math.radians(a)
    cos_val = math.cos(a)
    if abs(cos_val) < 1e-15:
        raise ValueError("Тангенс не определён для данного угла (cos = 0).")
    return math.tan(a)


def logarithm(a: float, base: float = 10.0) -> float:
    """Логарифм числа a по основанию base.

    Args:
        a: Аргумент логарифма.
        base: Основание логарифма (по умолчанию 10).

    Returns:
        Логарифм a по основанию base.

    Raises:
        ValueError: Если a <= 0 или base <= 0 или base == 1.
    """
    if a <= 0:
        raise ValueError("Логарифм определён только для положительных чисел.")
    if base <= 0 or base == 1:
        raise ValueError("Основание логарифма должно быть положительным и не равным 1.")
    return math.log(a, base)


def natural_log(a: float) -> float:
    """Натуральный логарифм (по основанию e).

    Args:
        a: Аргумент логарифма.

    Returns:
        Натуральный логарифм a.

    Raises:
        ValueError: Если a <= 0.
    """
    if a <= 0:
        raise ValueError("Логарифм определён только для положительных чисел.")
    return math.log(a)


def absolute(a: float) -> float:
    """Абсолютное значение (модуль) числа.

    Args:
        a: Число.

    Returns:
        Модуль a (|a|).
    """
    return abs(a)


def round_value(a: float, digits: int = 0) -> float:
    """Округление числа до указанного количества знаков.

    Args:
        a: Число для округления.
        digits: Количество знаков после запятой (по умолчанию 0).

    Returns:
        Округлённое значение a.
    """
    return round(a, int(digits))


# Словарь бинарных операций (для REPL-режима и токенизатора)
BINARY_OPERATIONS: dict[str, Callable[..., float]] = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
    "^": power,
    "**": power,
    "%": percent,
    "mod": modulo,
}

# Словарь унарных функций
UNARY_FUNCTIONS: dict[str, Callable[..., float]] = {
    "sqrt": sqrt,
    "!": factorial,
    "abs": absolute,
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "log": logarithm,
    "ln": natural_log,
    "round": round_value,
}

# Предопределённые константы
CONSTANTS: dict[str, float] = {
    "pi": math.pi,
    "e": math.e,
}