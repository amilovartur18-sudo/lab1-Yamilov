"""Калькулятор. Пиши сверху вниз: tokenize, потом validate, потом calculate.

Ядро только считает и возвращает число. Здесь нельзя вызывать input и print.
"""

from __future__ import annotations
from .errors import EmptyExpressionError, InvalidCharacterError,InvalidNumberError
def tokenize(expression: str) -> list[float | str]:
    if expression.strip() == "":
        raise EmptyExpressionError('Введите выражение')
    tokens: list[float| str] =[]
    i=0
    while i<len(expression):
        char=expression[i]
        if char ==" ":
            i=i+1
            continue
#continue это база без него "+" будет считаться как ошибка
#i=i+1 на пробеле нужен,чтобы сдвинуться с места/Если его убрать,то i навсегда останется в пробеле
        #проверка на унарный минус(пример -3 и 2*-3)
        number=''
        if char in '+-' and (len(tokens)==0 or (tokens[-1] in {'+','-','*','/'})):
            number=char
            i=i+1#чтобы не читать одно и тоже 2 раза
        if number!='' or char.isdigit():
            #проверка на дробные числа
            has_dot=False
            while i<len(expression) and (expression[i].isdigit() or (expression[i]==".")):
                if expression[i]=='.':
                    if has_dot==True:
                        raise InvalidNumberError('Недопустимая комбинация')
                    has_dot=True
                number=number+expression[i]
                i=i+1
            tokens.append(float(number))
            continue
        if char in "+-*/":
            tokens.append(char)
            i=i+1
            continue
        raise InvalidCharacterError('Недопустимый символ')
    return tokens
#это мы расссмотрели только целые числа,но не дробные
    

    """Разрежь строку на токены: числа как float, операторы как str."""


def validate(tokens: list[float | str]) -> None:
    
    """Проверь, что токены идут так: число, оператор, число, оператор, ..., число."""
    raise NotImplementedError


def calculate(tokens: list[float | str]) -> float:
    """Посчитай: сначала все * и /, потом все + и -."""
    raise NotImplementedError


def evaluate(expression: str) -> float:
    """Собери три шага выше в одну функцию."""
    raise NotImplementedError
