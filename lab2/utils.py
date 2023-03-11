import sys

import matplotlib.pyplot as plt
from typing import Callable


def find_roots_intervals(function: Callable[[float], float], a: float, b: float, eps: float = 0.01) -> list[
    tuple[float, float]]:
    intervals = []
    x = a
    right_y = function(x)
    while x < b:
        left_y = right_y
        right_y = function(x + eps)
        if left_y * right_y < 0:
            intervals.append((x, x + eps))
        x += eps
    return intervals


def create_graph(x: list[float], y: list[float], xlim: tuple[float, float], color: str) -> None:
    plt.plot(x, y, color=color)
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')
    plt.xlim(xlim)
    miny = sys.float_info.max
    maxy = sys.float_info.min
    for i in range(len(x)):
        if x[i] >= xlim[0]:
            if x[i] > xlim[1]:
                break
            if y[i] < miny:
                miny = y[i]
            if y[i] > maxy:
                maxy = y[i]

    plt.ylim((miny, maxy))
    plt.ylabel('y')
    plt.xlabel('x')
    plt.grid(True)
    plt.show()


def create_graph2(x1: list[float], y1: list[float], x2: list[float], y2: list[float], xlim: tuple[float, float],
                  color1: str, color2: str) -> None:
    plt.xlim(xlim)
    plt.ylim((-(xlim[1] - xlim[0]) / 2, (xlim[1] - xlim[0]) / 2))
    plt.scatter(x1, y1, color=color1, s=1)
    plt.scatter(x2, y2, color=color2, s=1)
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')
    plt.ylabel('x2')
    plt.xlabel('x1')
    plt.grid(True)
    plt.show()


def calculate_graph(function: Callable[[float], float],
                    a: float, b: float, step: float = 0.01) -> tuple[list[float], list[float]]:
    x = list()
    y = list()
    while a <= b:
        x.append(a)
        y.append(function(a))
        a += step
    return x, y


def calculate_graph2(function: Callable[[float, float], float],
                     a: float, b: float, step: float = 0.01) -> tuple[list[float], list[float]]:
    x = list()
    y = list()
    xc = a
    while xc <= b:
        yc = a
        while yc <= b:
            lb = function(xc, yc)
            lt = function(xc, yc + step)
            rb = function(xc + step, yc)
            rt = function(xc + step, yc + step)
            if (lb <= 0 or rb <= 0 or rt <= 0 or lt <= 0) and (lb >= 0 or rb >= 0 or rt >= 0 or lt >= 0):
                x.append(xc + step / 2)
                y.append(yc + step / 2)
            yc += step
        xc += step
    return x, y


def calculate_precision(eps: float, num_of_additional_digits: int = 1) -> int:
    if eps <= 0 or num_of_additional_digits < 0:
        raise ValueError("(ᇂ_Jᇂ )")
    precision: int = 0
    while eps < 1:
        eps *= 10
        precision += 1
    return precision + num_of_additional_digits


def derivative(function: Callable[[float], float], x: float, dx: float = 0.0000001) -> float:
    # who copies is the blonde
    return (function(x + dx) - function(x)) / dx


def derivative2(function: Callable[[float], float], x: float, dx: float = 0.0001) -> float:
    return (function(x + dx) + function(x - dx) - 2 * function(x)) / (dx ** 2)


def derivative_by_x1(function: Callable[[float, float], float], x1: float, x2: float, dx: float = 0.00000001) -> float:
    return (function(x1 + dx, x2) - function(x1, x2)) / dx


def derivative_by_x2(function: Callable[[float, float], float], x1: float, x2: float, dx: float = 0.00000001) -> float:
    return (function(x1, x2 + dx) - function(x1, x2)) / dx
