"""Конвертер величин. Пиши сам.

Группы: длина mm/cm/m/km, масса g/kg, температура c/f/k.
Разные группы смешивать нельзя. Ниже абсолютного нуля — ошибка.
"""

from __future__ import annotations


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Верни value, переведённое из from_unit в to_unit."""
    raise NotImplementedError
