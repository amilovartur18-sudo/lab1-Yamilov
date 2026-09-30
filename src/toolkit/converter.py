"""Конвертер единиц измерения.

Группы единиц:
- длина: mm, cm, m, km;
- масса: g, kg;
- температура: c, f, k.

Конвертация между разными группами запрещена.
Температура ниже абсолютного нуля запрещена.
"""

from __future__ import annotations

from .errors import (
    BelowAbsoluteZeroError,
    IncompatibleUnitsError,
    UnknownUnitError,
)

# Коэффициенты перевода длины в метры и массы в граммы.
_LENGTH_TO_METERS: dict[str, float] = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
}

_MASS_TO_GRAMS: dict[str, float] = {
    "g": 1.0,
    "kg": 1000.0,
}

_TEMPERATURE_UNITS = {"c", "f", "k"}

# Абсолютный ноль в каждой шкале.
_ABS_ZERO: dict[str, float] = {
    "k": 0.0,
    "c": -273.15,
    "f": -459.67,
}


def _normalize_unit(unit: str) -> str:
    """Привести единицу к нижнему регистру."""
    return unit.strip().lower()


def _find_group(unit: str) -> str:
    """Определить группу единицы: length, mass или temperature.

    :raises UnknownUnitError: единица неизвестна
    """
    if unit in _LENGTH_TO_METERS:
        return "length"
    if unit in _MASS_TO_GRAMS:
        return "mass"
    if unit in _TEMPERATURE_UNITS:
        return "temperature"
    raise UnknownUnitError(f"неизвестная единица: {unit!r}")


def _celsius_to_kelvin(value: float) -> float:
    return value + 273.15


def _fahrenheit_to_kelvin(value: float) -> float:
    return (value - 32.0) * 5.0 / 9.0 + 273.15


def _kelvin_to_celsius(value: float) -> float:
    return value - 273.15


def _kelvin_to_fahrenheit(value: float) -> float:
    return (value - 273.15) * 9.0 / 5.0 + 32.0


def _to_kelvin(value: float, unit: str) -> float:
    if unit == "k":
        return value
    if unit == "c":
        return _celsius_to_kelvin(value)
    return _fahrenheit_to_kelvin(value)


def _from_kelvin(value: float, unit: str) -> float:
    if unit == "k":
        return value
    if unit == "c":
        return _kelvin_to_celsius(value)
    return _kelvin_to_fahrenheit(value)


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Конвертировать значение из одной единицы в другую.

    :param value: числовое значение
    :param from_unit: исходная единица (регистр не важен)
    :param to_unit: целевая единица (регистр не важен)
    :return: результат как float
    :raises UnknownUnitError: неизвестная единица
    :raises IncompatibleUnitsError: разные группы единиц
    :raises BelowAbsoluteZeroError: температура ниже абсолютного нуля
    """
    src = _normalize_unit(from_unit)
    dst = _normalize_unit(to_unit)

    src_group = _find_group(src)
    dst_group = _find_group(dst)

    if src_group != dst_group:
        raise IncompatibleUnitsError(
            f"несовместимые единицы: {from_unit!r} и {to_unit!r}"
        )

    if src_group == "length":
        meters = value * _LENGTH_TO_METERS[src]
        return meters / _LENGTH_TO_METERS[dst]

    if src_group == "mass":
        grams = value * _MASS_TO_GRAMS[src]
        return grams / _MASS_TO_GRAMS[dst]

    # Температура: сначала в кельвины, проверка абсолютного нуля, потом в цель.
    kelvin = _to_kelvin(value, src)
    if kelvin < 0:
        raise BelowAbsoluteZeroError(
            f"температура ниже абсолютного нуля: {value} {src}"
        )
    # Также запретим исходное значение ниже абсолютного нуля в своей шкале
    # (на случай погрешностей — основная проверка уже через kelvin < 0).
    if value < _ABS_ZERO[src]:
        raise BelowAbsoluteZeroError(
            f"температура ниже абсолютного нуля: {value} {src}"
        )

    return _from_kelvin(kelvin, dst)
