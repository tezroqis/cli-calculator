#!/usr/bin/env python3
"""CLI Калькулятор — точка входа.

Запускает калькулятор в интерактивном режиме или вычисляет
переданное выражение.

Использование:
    python calc.py                    # REPL
    python calc.py "2 + 3 * 4"       # Одно выражение
    python calc.py -e "sqrt(16)"     # Явное выражение
    python calc.py -i                # Явный REPL
"""

from __future__ import annotations

from cli.interface import main_cli

if __name__ == "__main__":
    main_cli()