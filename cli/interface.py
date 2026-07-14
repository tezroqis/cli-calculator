"""Интерфейс командной строки калькулятора.

Поддерживает два режима:
  1. Интерактивный REPL (по умолчанию, или с флагом --interactive)
  2. Вычисление одного выражения (--expression "..." или позиционный аргумент)
"""

from __future__ import annotations

import argparse
import sys
from typing import NoReturn

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False
    # Заглушки для работы без colorama
    class _Fore:
        GREEN = ""
        RED = ""
        YELLOW = ""
        CYAN = ""
        RESET = ""

    class _Style:
        BRIGHT = ""
        RESET_ALL = ""

    Fore = _Fore()
    Style = _Style()


from core.evaluator import compute
from core.tokenizer import TokenizerError
from core.parser import ParserError
from core.evaluator import EvaluatorError


# История вычислений (для REPL)
_history: list[str] = []


def _print_colored(text: str, color: str = "", bold: bool = False) -> None:
    """Выводит текст с опциональным цветом.

    Args:
        text: Текст для вывода.
        color: Код цвета (используется Fore из colorama).
        bold: Если True, делает текст жирным.
    """
    if HAS_COLORAMA:
        prefix = Style.BRIGHT if bold else ""
        suffix = Style.RESET_ALL
        print(f"{prefix}{color}{text}{suffix}")
    else:
        print(text)


def run_repl() -> None:
    """Запускает интерактивный REPL-режим калькулятора."""
    _print_colored("=" * 50, Fore.CYAN)
    _print_colored("CLI Калькулятор v2.0", Fore.CYAN, bold=True)
    _print_colored("=" * 50, Fore.CYAN)
    print()
    print("Введите математическое выражение и нажмите Enter.")
    print("Поддерживаются: +, -, *, /, ^, %, mod, sqrt, sin, cos, tan,")
    print("               log, ln, abs, round, factorial, !, pi, e, скобки")
    print("Специальные команды:")
    print("  :h, :help   — показать эту справку")
    print("  :hist       — показать историю вычислений")
    print("  :q, :quit   — выход")
    print()

    while True:
        try:
            prompt_color = Fore.GREEN if HAS_COLORAMA else ""
            prompt_reset = Style.RESET_ALL if HAS_COLORAMA else ""
            expression = input(f"{prompt_color}>>> {prompt_reset}").strip()

            if not expression:
                continue

            # Обработка команд
            if expression.startswith(":"):
                _handle_command(expression.lower())
                continue

            # Сохраняем в историю
            _history.append(expression)

            # Вычисление
            result = compute(expression)

            # Форматирование результата
            if result == int(result):
                result_str = str(int(result))
            else:
                result_str = f"{result:.10g}"

            _print_colored(f"  = {result_str}", Fore.GREEN, bold=True)

        except TokenizerError as e:
            _print_colored(f"  Ошибка: {e}", Fore.RED)
        except ParserError as e:
            _print_colored(f"  Синтаксическая ошибка: {e}", Fore.RED)
        except EvaluatorError as e:
            _print_colored(f"  Ошибка вычисления: {e}", Fore.RED)
        except ZeroDivisionError as e:
            _print_colored(f"  Ошибка: {e}", Fore.RED)
        except ValueError as e:
            _print_colored(f"  Ошибка: {e}", Fore.RED)
        except (KeyboardInterrupt, EOFError):
            _print_colored("\nДо свидания!", Fore.YELLOW)
            break
        except Exception as e:
            _print_colored(f"  Неизвестная ошибка: {e}", Fore.RED)


def _handle_command(command: str) -> None:
    """Обрабатывает специальные команды REPL.

    Args:
        command: Строка команды (начинается с ':').
    """
    cmd = command.lstrip(":")

    if cmd in ("h", "help"):
        print()
        print("Поддерживаемые операции и функции:")
        print("  +, -, *, /     — базовые арифметические")
        print("  ^ или **       — возведение в степень")
        print("  %              — процент (a% от b)")
        print("  mod            — остаток от деления")
        print("  sqrt(x)        — квадратный корень")
        print("  abs(x)         — модуль числа")
        print("  sin(x), cos(x), tan(x) — тригонометрия (радианы)")
        print("  log(x), ln(x)  — логарифмы (log — по основанию 10)")
        print("  round(x)       — округление до целого")
        print("  factorial(x), x! — факториал")
        print("  pi, e          — константы")
        print("  ( )            — скобки для группировки")
        print()

    elif cmd == "hist":
        if not _history:
            print("  История пуста.")
        else:
            for i, expr in enumerate(_history, 1):
                print(f"  {i}: {expr}")

    elif cmd in ("q", "quit"):
        _print_colored("До свидания!", Fore.YELLOW)
        sys.exit(0)

    else:
        print(f"  Неизвестная команда: :{cmd}")
        print("  Доступные команды: :help, :hist, :quit")


def run_expression(expression: str) -> None:
    """Вычисляет одно выражение и выводит результат.

    Args:
        expression: Строка математического выражения.
    """
    try:
        result = compute(expression)

        if result == int(result):
            print(int(result))
        else:
            print(f"{result:.10g}")

    except TokenizerError as e:
        _print_colored(f"Ошибка: {e}", Fore.RED)
        sys.exit(1)
    except ParserError as e:
        _print_colored(f"Синтаксическая ошибка: {e}", Fore.RED)
        sys.exit(1)
    except EvaluatorError as e:
        _print_colored(f"Ошибка вычисления: {e}", Fore.RED)
        sys.exit(1)
    except ZeroDivisionError as e:
        _print_colored(f"Ошибка: {e}", Fore.RED)
        sys.exit(1)
    except ValueError as e:
        _print_colored(f"Ошибка: {e}", Fore.RED)
        sys.exit(1)


def build_argument_parser() -> argparse.ArgumentParser:
    """Создаёт парсер аргументов командной строки.

    Returns:
        Настроенный ArgumentParser.
    """
    parser = argparse.ArgumentParser(
        prog="calc",
        description="CLI Калькулятор — вычисление математических выражений",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  calc                          # Запуск в интерактивном режиме
  calc "2 + 3 * 4"             # Вычисление выражения
  calc -e "sqrt(16) + sin(pi/2)"  # Явное указание выражения
  calc --interactive           # Явный запуск REPL
        """,
    )

    parser.add_argument(
        "expression",
        nargs="?",
        help="Математическое выражение для вычисления (если не указано, запускается REPL)",
    )

    parser.add_argument(
        "-e", "--expression",
        dest="expr",
        help="Математическое выражение для вычисления",
    )

    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Запустить интерактивный режим (REPL)",
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Отключить цветной вывод",
    )

    return parser


def main_cli() -> NoReturn:
    """Точка входа CLI-калькулятора.

    Разбирает аргументы и запускает соответствующий режим.
    """
    parser = build_argument_parser()
    args = parser.parse_args()

    # Отключение цветного вывода
    global HAS_COLORAMA
    if args.no_color:
        HAS_COLORAMA = False

    # Определяем, что делать
    expression = args.expr or args.expression

    if args.interactive or (expression is None and not args.expr):
        run_repl()
    else:
        run_expression(expression)

    sys.exit(0)