"""Калькулятор арифметических выражений.

Разбор делится на три этапа:
1. tokenize  — строка → список токенов (числа и операторы);
2. validate  — проверка, что последовательность токенов корректна;
3. calculate — вычисление: сначала * и /, потом + и -.

Унарный +/− «прилипает» к числу на этапе tokenize,
поэтому выражение ``2*-3`` становится токенами ``[2, '*', -3]``.
"""

from __future__ import annotations

from .errors import (
    ConsecutiveOperatorsError,
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidCharacterError,
    InvalidNumberError,
    MissingOperandError,
)

# Бинарные операторы и их приоритет (чем больше число — тем выше приоритет).
_PRECEDENCE: dict[str, int] = {"+": 1, "-": 1, "*": 2, "/": 2}
_OPERATORS = set(_PRECEDENCE)


def tokenize(expression: str) -> list[float | str]:
    """Разбить строку выражения на числа и операторы.

    Пробелы игнорируются. Унарный ``+``/``-`` перед числом
    (в начале выражения или сразу после оператора) входит в число.

    :param expression: исходная строка выражения
    :return: список токенов: ``float`` для чисел, ``str`` для операторов
    :raises EmptyExpressionError: строка пустая или только из пробелов
    :raises InvalidCharacterError: встретился недопустимый символ
    :raises InvalidNumberError: число нельзя преобразовать в float
    :raises MissingOperandError: унарный знак без числа после него
    """
    if expression.strip() == "":
        raise EmptyExpressionError("пустое выражение")

    tokens: list[float | str] = []
    i = 0
    length = len(expression)

    while i < length:
        char = expression[i]

        # Пробелы пропускаем.
        if char.isspace():
            i += 1
            continue

        # Число (возможно с унарным знаком).
        # Унарный знак — если мы в начале или предыдущий токен был оператором.
        is_unary = char in "+-" and (
            len(tokens) == 0 or tokens[-1] in _OPERATORS
        )
        if char.isdigit() or char == "." or is_unary:
            start = i
            # Унарный знак — один символ, дальше обязательно цифра или точка.
            if is_unary:
                i += 1
                next_ok = i < length and (
                    expression[i].isdigit() or expression[i] == "."
                )
                if not next_ok:
                    raise MissingOperandError(
                        f"ожидалось число после унарного знака на позиции {start}"
                    )

            # Собираем цифры и одну точку.
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
            # Одиночный "+" или "-" уже отсеяны выше; "." без цифр — ошибка.
            if raw in {".", "+", "-", "+.", "-."}:
                raise InvalidNumberError(f"некорректное число: {raw!r}")
            try:
                tokens.append(float(raw))
            except ValueError as exc:
                raise InvalidNumberError(f"некорректное число: {raw!r}") from exc
            continue

        # Бинарный оператор.
        if char in _OPERATORS:
            tokens.append(char)
            i += 1
            continue

        raise InvalidCharacterError(f"недопустимый символ: {char!r}")

    if not tokens:
        raise EmptyExpressionError("пустое выражение")

    return tokens


def validate(tokens: list[float | str]) -> None:
    """Проверить, что токены образуют корректное выражение.

    Ожидаемый вид: число, оператор, число, оператор, ..., число.

    :param tokens: список токенов после tokenize
    :raises MissingOperandError: выражение начинается/заканчивается оператором
    :raises ConsecutiveOperatorsError: два оператора подряд
    """
    expect_number = True
    for token in tokens:
        if expect_number:
            if not isinstance(token, float):
                # Оператор там, где ждали число.
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

    # Если цикл закончился ожиданием числа — выражение оборвалось на операторе.
    if expect_number:
        raise MissingOperandError("выражение обрывается на операторе")


def _apply(operator: str, left: float, right: float) -> float:
    """Применить бинарный оператор к двум числам."""
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
    # Сюда не должны попадать — validate пропускает только известные операторы.
    raise InvalidCharacterError(f"неизвестный оператор: {operator!r}")


def calculate(tokens: list[float | str]) -> float:
    """Вычислить значение по списку токенов в два прохода.

    Первый проход: все ``*`` и ``/`` (высокий приоритет).
    Второй проход: все ``+`` и ``-`` (низкий приоритет).

    :param tokens: проверенный список токенов
    :return: результат вычисления
    :raises DivisionByZeroError: деление на ноль
    """
    # --- Проход 1: умножение и деление ---------------------------------
    first_pass: list[float | str] = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token in {"*", "/"}:
            # left уже лежит в first_pass; right — следующий токен.
            left = first_pass.pop()
            right = tokens[i + 1]
            assert isinstance(left, float)
            assert isinstance(right, float)
            first_pass.append(_apply(str(token), left, right))
            i += 2
        else:
            first_pass.append(token)
            i += 1

    # --- Проход 2: сложение и вычитание --------------------------------
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
    """Полный цикл: tokenize → validate → calculate.

    Это единственная функция, которую должен вызывать CLI.
    Ядро только считает и возвращает число (без интерактивного ввода/вывода).

    :param expression: строка выражения, например ``"2+3*4"``
    :return: числовой результат
    """
    tokens = tokenize(expression)
    validate(tokens)
    return calculate(tokens)
