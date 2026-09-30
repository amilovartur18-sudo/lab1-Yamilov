"""Пользовательские исключения пакета toolkit.

Все ошибки от некорректного ввода наследуются от ToolkitError.
CLI ловит их одним except, пишет сообщение в stderr и завершается с кодом 2.
"""


class ToolkitError(Exception):
    """Базовый класс для всех ошибок пакета toolkit."""


# --- Ошибки калькулятора -----------------------------------------------

class EmptyExpressionError(ToolkitError):
    """Выражение пустое или состоит только из пробелов."""


class InvalidCharacterError(ToolkitError):
    """В выражении встретился символ, не входящий в допустимый набор."""


class MissingOperandError(ToolkitError):
    """Оператору не хватает операнда (например, выражение обрывается)."""


class ConsecutiveOperatorsError(ToolkitError):
    """Два бинарных оператора подряд без операнда между ними."""


class DivisionByZeroError(ToolkitError):
    """Попытка деления на ноль."""


class InvalidNumberError(ToolkitError):
    """Токен похож на число, но не может быть преобразован в float."""


# --- Ошибки конвертера ---------------------------------------------------

class UnknownUnitError(ToolkitError):
    """Указана единица измерения, которой нет ни в одной группе."""


class IncompatibleUnitsError(ToolkitError):
    """Единицы измерения принадлежат разным группам (например, kg и m)."""


class BelowAbsoluteZeroError(ToolkitError):
    """Температура (в пересчёте на Кельвины) ниже абсолютного нуля."""
