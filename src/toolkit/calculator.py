"""Калькулятор арифметических выражений."""

from __future__ import annotations

from .errors import (
    ConsecutiveOperatorsError,
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidCharacterError,
    InvalidNumberError,
    MissingOperandError,
)

_PRECEDENCE: dict[str, int] = {"+": 1, "-": 1, "*": 2, "/": 2}
_OPERATORS = set(_PRECEDENCE)


def tokenize(expression: str) -> list[float | str]:
    """преобразование строки '2*-3' -> [2.0, '*', -3.0]"""
    if expression.strip() == "":
        raise EmptyExpressionError("пустое выражение")

    tokens: list[float | str] = []
    i = 0
    length = len(expression)

    while i < length:
        char = expression[i]

        if char.isspace():
            i += 1
            continue

        is_unary = char in "+-" and (
            len(tokens) == 0 or tokens[-1] in _OPERATORS
        )
        if char.isdigit() or char == "." or is_unary:
            start = i
            if is_unary:
                i += 1
                next_ok = i < length and (
                    expression[i].isdigit() or expression[i] == "."
                )
                if not next_ok:
                    raise MissingOperandError(
                        f"ожидалось число после унарного знака на позиции {start}"
                    )

            has_dot = False
            while i < length and (expression[i].isdigit() or expression[i] == "."):
                if expression[i] == ".":
                    if has_dot:
                        raise InvalidNumberError(
                            f"некорректное число около позиции {start}"
                        )
                    has_dot = True
                i += 1

            raw = expression[start:i]
            if raw in {".", "+", "-", "+.", "-."}:
                raise InvalidNumberError(f"некорректное число: {raw!r}")
            try:
                tokens.append(float(raw))
            except ValueError as exc:
                raise InvalidNumberError(f"некорректное число: {raw!r}") from exc
            continue

        if char in _OPERATORS:
            tokens.append(char)
            i += 1
            continue

        raise InvalidCharacterError(f"недопустимый символ: {char!r}")

    if not tokens:
        raise EmptyExpressionError("пустое выражение")

    return tokens


def validate(tokens: list[float | str]) -> None:
    """проверка корректности токенов в выражении"""
    expect_number = True
    for token in tokens:
        if expect_number:
            if not isinstance(token, float):
                if token in _OPERATORS:
                    raise ConsecutiveOperatorsError(
                        f"пропущен операнд перед оператором {token!r}"
                    )
                raise MissingOperandError("ожидалось число")
            expect_number = False
        else:
            if token not in _OPERATORS:
                raise MissingOperandError("ожидался оператор между числами")
            expect_number = True

    if expect_number:
        raise MissingOperandError("выражение обрывается на операторе")


def _apply(operator: str, left: float, right: float) -> float:
    """применить знак к двум числам"""
    if operator == "+":
        return left + right
    if operator == "-":
        return left - right
    if operator == "*":
        return left * right
    if operator == "/":
        if right == 0:
            raise DivisionByZeroError("деление на ноль")
        return left / right
    raise InvalidCharacterError(f"неизвестный оператор: {operator!r}")


def calculate(tokens: list[float | str]) -> float:
    """вычислить значение по списку токенов"""
    first_pass: list[float | str] = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token in {"*", "/"}:
            left = first_pass.pop()
            right = tokens[i + 1]
            assert isinstance(left, float)
            assert isinstance(right, float)
            first_pass.append(_apply(str(token), left, right))
            i += 2
        else:
            first_pass.append(token)
            i += 1

    result = first_pass[0]
    assert isinstance(result, float)
    i = 1
    while i < len(first_pass):
        operator = first_pass[i]
        right = first_pass[i + 1]
        assert isinstance(operator, str)
        assert isinstance(right, float)
        result = _apply(operator, result, right)
        i += 2

    return result


def evaluate(expression: str) -> float:
    """полный расчёт выражения"""
    tokens = tokenize(expression)
    validate(tokens)
    return calculate(tokens)
