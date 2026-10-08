"""Командная строка: python -m toolkit ...

Напиши сам. Успех — код 0. Ошибка пользователя — текст в stderr и код 2.
"""

from __future__ import annotations


def main(argv: list[str] | None = None) -> int:
    """Разбери команду и вызови калькулятор или конвертер."""
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
