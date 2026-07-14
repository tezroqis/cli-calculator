"""Тесты для модуля математических операций."""

from __future__ import annotations

import math
import pytest

from core.operations import (
    add,
    subtract,
    multiply,
    divide,
    power,
    sqrt,
    factorial,
    modulo,
    percent,
    sin,
    cos,
    tan,
    logarithm,
    natural_log,
    absolute,
    round_value,
    CONSTANTS,
)


class TestBasicArithmetic:
    """Тесты базовых арифметических операций."""

    def test_add_positive(self) -> None:
        assert add(2.0, 3.0) == 5.0
        assert add(-1.0, 1.0) == 0.0
        assert add(0.0, 0.0) == 0.0

    def test_add_floats(self) -> None:
        assert abs(add(0.1, 0.2) - 0.3) < 1e-15

    def test_subtract(self) -> None:
        assert subtract(5.0, 3.0) == 2.0
        assert subtract(3.0, 5.0) == -2.0
        assert subtract(0.0, 0.0) == 0.0

    def test_multiply(self) -> None:
        assert multiply(2.0, 3.0) == 6.0
        assert multiply(-2.0, 3.0) == -6.0
        assert multiply(0.0, 5.0) == 0.0

    def test_divide(self) -> None:
        assert divide(6.0, 3.0) == 2.0
        assert divide(5.0, 2.0) == 2.5
        assert divide(-6.0, 2.0) == -3.0

    def test_divide_by_zero(self) -> None:
        with pytest.raises(ZeroDivisionError, match="Деление на ноль"):
            divide(1.0, 0.0)


class TestPower:
    """Тесты возведения в степень."""

    def test_power_positive(self) -> None:
        assert power(2.0, 3.0) == 8.0
        assert power(5.0, 0.0) == 1.0

    def test_power_negative_base(self) -> None:
        assert power(-2.0, 3.0) == -8.0
        assert power(-2.0, 2.0) == 4.0

    def test_power_fractional(self) -> None:
        assert abs(power(4.0, 0.5) - 2.0) < 1e-15
        assert abs(power(9.0, 0.5) - 3.0) < 1e-15


class TestSqrt:
    """Тесты квадратного корня."""

    def test_sqrt_positive(self) -> None:
        assert sqrt(4.0) == 2.0
        assert sqrt(9.0) == 3.0
        assert sqrt(2.25) == 1.5

    def test_sqrt_zero(self) -> None:
        assert sqrt(0.0) == 0.0

    def test_sqrt_negative(self) -> None:
        with pytest.raises(ValueError, match="отрицательного числа"):
            sqrt(-1.0)


class TestFactorial:
    """Тесты факториала."""

    def test_factorial_small(self) -> None:
        assert factorial(0.0) == 1.0
        assert factorial(1.0) == 1.0
        assert factorial(5.0) == 120.0

    def test_factorial_negative(self) -> None:
        with pytest.raises(ValueError, match="отрицательного"):
            factorial(-1.0)

    def test_factorial_non_integer(self) -> None:
        with pytest.raises(ValueError, match="целых"):
            factorial(3.5)


class TestModulo:
    """Тесты остатка от деления."""

    def test_modulo_positive(self) -> None:
        assert modulo(10.0, 3.0) == 1.0
        assert modulo(7.0, 2.0) == 1.0
        assert modulo(6.0, 3.0) == 0.0

    def test_modulo_by_zero(self) -> None:
        with pytest.raises(ZeroDivisionError):
            modulo(5.0, 0.0)


class TestPercent:
    """Тесты процентов."""

    def test_percent(self) -> None:
        assert percent(10.0, 200.0) == 20.0
        assert percent(50.0, 100.0) == 50.0
        assert percent(0.0, 100.0) == 0.0


class TestTrigonometry:
    """Тесты тригонометрических функций."""

    def test_sin(self) -> None:
        assert abs(sin(0.0)) < 1e-15
        assert abs(sin(math.pi / 2) - 1.0) < 1e-15
        assert abs(sin(math.pi)) < 1e-15

    def test_cos(self) -> None:
        assert abs(cos(0.0) - 1.0) < 1e-15
        assert abs(cos(math.pi)) + 1.0 < 1e-15

    def test_tan(self) -> None:
        assert abs(tan(0.0)) < 1e-15
        assert abs(tan(math.pi / 4) - 1.0) < 1e-15

    def test_tan_undefined(self) -> None:
        with pytest.raises(ValueError, match="Тангенс не определён"):
            tan(math.pi / 2)

    def test_sin_degrees(self) -> None:
        assert abs(sin(90.0, radians=False) - 1.0) < 1e-15
        assert abs(sin(0.0, radians=False)) < 1e-15

    def test_cos_degrees(self) -> None:
        assert abs(cos(180.0, radians=False) + 1.0) < 1e-15


class TestLogarithms:
    """Тесты логарифмов."""

    def test_logarithm_base10(self) -> None:
        assert abs(logarithm(100.0) - 2.0) < 1e-15
        assert abs(logarithm(1.0)) < 1e-15

    def test_logarithm_custom_base(self) -> None:
        assert abs(logarithm(8.0, 2.0) - 3.0) < 1e-15

    def test_logarithm_non_positive(self) -> None:
        with pytest.raises(ValueError, match="положительных"):
            logarithm(0.0)
        with pytest.raises(ValueError, match="положительных"):
            logarithm(-1.0)

    def test_logarithm_invalid_base(self) -> None:
        with pytest.raises(ValueError, match="Основание"):
            logarithm(10.0, -1.0)

    def test_natural_log(self) -> None:
        assert abs(natural_log(math.e) - 1.0) < 1e-15
        assert abs(natural_log(1.0)) < 1e-15

    def test_natural_log_non_positive(self) -> None:
        with pytest.raises(ValueError):
            natural_log(-1.0)


class TestAbsolute:
    """Тесты модуля числа."""

    def test_absolute_positive(self) -> None:
        assert absolute(5.0) == 5.0
        assert absolute(-5.0) == 5.0
        assert absolute(0.0) == 0.0


class TestRound:
    """Тесты округления."""

    def test_round_integer(self) -> None:
        assert round_value(3.7) == 4.0
        assert round_value(3.2) == 3.0

    def test_round_digits(self) -> None:
        assert round_value(3.14159, 2) == 3.14


class TestConstants:
    """Тесты констант."""

    def test_pi(self) -> None:
        assert abs(CONSTANTS["pi"] - 3.141592653589793) < 1e-15

    def test_e(self) -> None:
        assert abs(CONSTANTS["e"] - 2.718281828459045) < 1e-15