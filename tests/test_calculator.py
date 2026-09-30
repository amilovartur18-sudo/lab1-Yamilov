"""Тесты калькулятора (ядро, без subprocess)."""

import pytest

from toolkit.calculator import calculate, evaluate, tokenize, validate
from toolkit.errors import (
    ConsecutiveOperatorsError,
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidCharacterError,
    MissingOperandError,
)

# --- Позитивные тесты ----------------------------------------------------

def test_addition_and_multiplication_priority() -> None:
    """2+3*4 → 14: умножение раньше сложения."""
    assert evaluate("2+3*4") == 14


def test_division_gives_float() -> None:
    """10 / 4 → 2.5."""
    assert evaluate("10 / 4") == 2.5


def test_unary_minus_after_operator() -> None:
    """2 * -3 → -6: унарный минус «прилипает» к числу."""
    assert evaluate("2 * -3") == -6


def test_spaces_are_ignored() -> None:
    """Пробелы между токенами не влияют на результат."""
    assert evaluate("  1 +  2  ") == 3


def test_floats_and_chain() -> None:
    """Вещественные числа и цепочка операций."""
    assert evaluate("1.5 + 2.5 * 2") == 6.5


def test_unary_plus_minus_at_start() -> None:
    """Унарный знак в начале выражения."""
    assert evaluate("-5+3") == -2
    assert evaluate("+7") == 7


# --- Негативные тесты ----------------------------------------------------

def test_empty_expression_error() -> None:
    with pytest.raises(EmptyExpressionError):
        evaluate("")


def test_whitespace_only_error() -> None:
    with pytest.raises(EmptyExpressionError):
        evaluate("   ")


def test_invalid_character_error() -> None:
    with pytest.raises(InvalidCharacterError):
        evaluate("2+a")


def test_consecutive_operators_error() -> None:
    with pytest.raises(ConsecutiveOperatorsError):
        evaluate("2*/3")


def test_division_by_zero_error() -> None:
    with pytest.raises(DivisionByZeroError):
        evaluate("1/0")


def test_missing_operand_at_end() -> None:
    with pytest.raises(MissingOperandError):
        evaluate("2+")


def test_tokenize_attaches_unary_minus() -> None:
    """Для защиты: 2*-3 → токены [2, '*', -3]."""
    tokens = tokenize("2*-3")
    assert tokens == [2.0, "*", -3.0]
    validate(tokens)
    assert calculate(tokens) == -6.0
