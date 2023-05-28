import math
from typing import Callable


class Equation:
    def __init__(self, orig: Callable[[float, float], float], text_orig: str,
                 derivative: Callable[[float, float], float], text_derivative: str):
        self.orig = orig
        self.text_orig = text_orig
        self.derivative = derivative
        self.text_derivative = text_derivative

    def orig(self, x: float, c: float) -> float:
        return self.orig(x, c)

    def __call__(self, x: float, y: float) -> float:
        return self.derivative(x, y)

    def orig_str(self, c: float = 0.0):
        if c < 0:
            return self.text_orig.lower().replace("+c", f"{c:.3f}")
        return self.text_orig.lower().replace("c", f"{c:.3f}")

    def derivative_str(self):
        return self.text_derivative

    def __str__(self):
        return "y' = " + self.text_derivative


equations = [
    Equation(lambda x, c: -(math.e ** x / (x * math.e ** x + c)), "-e^x / (x * e^x+C)",
             lambda x, y: y + (x + 1) * y ** 2, "y+(x+1)y^2"),

]
