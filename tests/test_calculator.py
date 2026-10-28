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


def test_addition_and_multiplication_priority() -> None:
    assert evaluate("2+3*4") == 14


def test_division_gives_float() -> None:
    assert evaluate("10 / 4") == 2.5


def test_unary_minus_after_operator() -> None:
    assert evaluate("2 * -3") == -6


def test_spaces_are_ignored() -> None:
    assert evaluate("  1 +  2  ") == 3


def test_floats_and_chain() -> None:
    assert evaluate("1.5 + 2.5 * 2") == 6.5


def test_unary_plus_minus_at_start() -> None:
    assert evaluate("-5+3") == -2
    assert evaluate("+7") == 7


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
    tokens = tokenize("2*-3")
    assert tokens == [2.0, "*", -3.0]
    validate(tokens)
    assert calculate(tokens) == -6.0
