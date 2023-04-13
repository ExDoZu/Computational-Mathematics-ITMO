from typing import Callable


def total_rectangles_area(function: Callable[[float], float], x0: float, h: float, n: int):
    ys = 0
    for i in range(n):
        ys += function(x0)
        x0 += h
    return ys * h


def step(a: float, b: float, n: int):
    return (b - a) / n


class Method:
    def __init__(self, method: Callable[[Callable[[float], float], float, float, int], float], text: str):
        self.method = method
        self.text = text

    def __call__(self, function: Callable[[float], float], a: float, b: float, n: int):
        return self.method(function, a, b, n)

    def __str__(self):
        return self.text


def left_rectangles(function: Callable[[float], float], a: float, b: float, n: int):
    h = step(a, b, n)
    x0 = a
    return total_rectangles_area(function, x0, h, n)


def right_rectangles(function: Callable[[float], float], a: float, b: float, n: int):
    h = step(a, b, n)
    x0 = a + h
    return total_rectangles_area(function, x0, h, n)


def middle_rectangles(function: Callable[[float], float], a: float, b: float, n: int):
    h = step(a, b, n)
    x0 = a + h / 2
    return total_rectangles_area(function, x0, h, n)


def trapezoid(function: Callable[[float], float], a: float, b: float, n: int):
    h = step(a, b, n)
    x0 = a + h
    s = total_rectangles_area(function, x0, h, n - 1)
    return h * ((function(a) + function(b)) / 2) + s


def simpson(function: Callable[[float], float], a: float, b: float, n: int):
    if n % 2 != 0:
        raise ValueError('n must be even')
    h = (b - a) / n
    ys = 0
    for i in range(1, n):
        if i % 2 == 0:
            ys += 2 * function(a + i * h)
        else:
            ys += 4 * function(a + i * h)
    return h / 3 * (function(a) + ys + function(b))


methods = [
    Method(left_rectangles, "Метод левых прямоугольников"),
    Method(right_rectangles, "Метод правых прямоугольников"),
    Method(middle_rectangles, "Метод средних прямоугольников"),
    Method(trapezoid, "Метод трапеций"),
    Method(simpson, "Метод Симпсона"),
]
