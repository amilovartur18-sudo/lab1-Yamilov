"""Точка входа по требованиям шаблона репозитория.

Запускает тот же CLI, что и ``python -m toolkit``.
"""

from toolkit.__main__ import main

if __name__ == "__main__":
    raise SystemExit(main())
