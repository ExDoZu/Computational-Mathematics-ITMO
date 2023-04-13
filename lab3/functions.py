import math
from typing import Callable


class Function:
    def __init__(self, func: Callable[[float], float], text: str):
        self.func = func
        self.text = text

    def __call__(self, x: float):
        try:
            return self.func(x)
        except (ValueError, ZeroDivisionError):
            return 0

    def __str__(self):
        return self.text


functions = [
    Function(lambda x: -2 * x ** 3 - 5 * x ** 2 + 7 * x - 13, "-2x^3 - 5x^2 + 7x - 13"),
    Function(lambda x: x ** 2, "x^2"),
    Function(lambda x: math.sin(x ** 3), "sin(x^3)"),
    Function(lambda x: 6 * x ** 6 - 5 * x ** 5 + 4 * x ** 4 - 3 * x ** 3 + 2 * x ** 2 - x + 1,
             "6x^6-5x^5+4x^4-3x^3+2x^2-x+1"),
    Function(lambda x: math.log(abs(x)), "ln(|x|)"),
    Function(lambda x: 1 / x, "1/x"),
]
