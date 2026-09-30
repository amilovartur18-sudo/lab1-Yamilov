"""Тесты конвертера величин."""

import pytest

from toolkit.converter import convert
from toolkit.errors import (
    BelowAbsoluteZeroError,
    IncompatibleUnitsError,
    UnknownUnitError,
)


def test_mm_to_m() -> None:
    assert convert(1000, "mm", "m") == 1.0


def test_kg_to_g() -> None:
    assert convert(1.5, "kg", "g") == 1500.0


def test_celsius_to_fahrenheit() -> None:
    assert convert(0, "c", "f") == 32.0


def test_celsius_to_kelvin() -> None:
    """0 °C = 273.15 K; абсолютный ноль −273.15 °C = 0 K."""
    assert convert(0, "c", "k") == pytest.approx(273.15)
    assert convert(-273.15, "c", "k") == pytest.approx(0.0)


def test_case_insensitive_units() -> None:
    assert convert(1000, "MM", "M") == 1.0


def test_below_absolute_zero() -> None:
    with pytest.raises(BelowAbsoluteZeroError):
        convert(-300, "c", "k")


def test_incompatible_units() -> None:
    with pytest.raises(IncompatibleUnitsError):
        convert(1, "kg", "m")


def test_unknown_unit() -> None:
    with pytest.raises(UnknownUnitError):
        convert(1, "xyz", "m")
