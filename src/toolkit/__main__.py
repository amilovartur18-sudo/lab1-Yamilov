"""Точка входа: ``python -m toolkit ...``.

CLI только парсит аргументы, вызывает ядро и печатает результат.
Вычислительное ядро (calculator / converter) не использует input/print.
"""

from __future__ import annotations

import argparse
import sys

from .calculator import evaluate
from .converter import convert
from .errors import ToolkitError


def build_parser() -> argparse.ArgumentParser:
    """Собрать парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="Консольный калькулятор и конвертер величин",
    )
    subparsers = parser.add_subparsers(dest="command")

    calc_parser = subparsers.add_parser("calc", help="вычислить выражение")
    calc_parser.add_argument("expression", help='выражение, например "2+3*4"')

    convert_parser = subparsers.add_parser("convert", help="конвертировать величину")
    convert_parser.add_argument("value", type=float, help="числовое значение")
    convert_parser.add_argument(
        "--from",
        dest="from_unit",
        required=True,
        help="исходная единица",
    )
    convert_parser.add_argument(
        "--to",
        dest="to_unit",
        required=True,
        help="целевая единица",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Запустить CLI.

    :param argv: аргументы (по умолчанию sys.argv[1:])
    :return: код выхода — 0 при успехе, 2 при пользовательской ошибке
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    try:
        if args.command == "calc":
            result = evaluate(args.expression)
            print(result)
            return 0

        if args.command == "convert":
            result = convert(args.value, args.from_unit, args.to_unit)
            print(result)
            return 0
    except ToolkitError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
