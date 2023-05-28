import matplotlib.pyplot as plt
import numpy as np
import sympy
from equations import *
from methods import *
from utils import *

eq = choose("уравнение", equations)
orig = eq.orig

x0 = read_number("Введите x0: ")
xn = read_number("Введите xn: ")
y0 = read_number("Введите y0: ")
h = read_number("Введите шаг: ")
eps = read_number("Введите точность: ")
c = sympy.symbols("c")
c = sympy.solve(orig(x0, c) - y0, c)[0]  # constant


def solve(x0: float, y0: float, h: float, xn: float, eq: Equation, method: Method, plt):
    print(method)
    points = method(x0, y0, h, xn, eq)
    if method.name == "Метод Эйлера":
        p = 1
    elif method.name == "Мод. метод Эйлера":
        p = 2
    elif method.name == "Метод Рунге-Кутты 4 порядка":
        p = 4
    else:
        p = 0
        r = -1
    if p != 0:
        h_half = h / 2
        points_half = method(x0, y0, h_half, xn, eq)
        while abs(points[-1][1] - points_half[-1][1]) / (2 ** p - 1) > eps:
            points = points_half
            h_half = h / 2
            points_half = method(x0, y0, h_half, xn, eq)
        r = abs(points[-1][1] - points_half[-1][1]) / (2 ** p - 1)

    print_points(points)
    if r != -1:
        print(f"R = {r} <= {eps}")
    plt.plot(np.array(points)[:, 0], np.array(points)[:, 1], label=method)
    return points


print("Истинное решение")
print("y =", eq.orig_str(c))
orig_points = [(x, orig(x, c)) for x in np.arange(x0, xn + 1e-6, h)]
print_points(orig_points)
orig_graph_points = [(x, orig(x, c)) for x in np.arange(x0, xn + 1e-6, h / 100)]
plt.plot(np.array(orig_graph_points)[:, 0], np.array(orig_graph_points)[:, 1], label=eq.orig_str(c))

for method in methods:
    ys = np.array(solve(x0, y0, h, xn + 1e-9, eq, method, plt))[:, 1]
    if method.name == "Метод Милна" or method.name == "Метод Адамса":
        print(f"eps = {max(abs(ys - np.array(orig_points)[:, 1]))}")

plt.legend()
plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')
plt.grid()
plt.show()
