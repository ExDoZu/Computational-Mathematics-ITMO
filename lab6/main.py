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

n = int((xn + 1e-9 - x0) / h)
new_xn = x0 + n * h
if new_xn < xn:
    xn = new_xn + h
    print(f"xn изменено на {xn:.6f}, так как длина интервала не кратна шагу", end="\n\n")
else:
    xn = new_xn


def solve(x0: float, y0: float, h: float, xn: float, eq: Equation, method: Method, plt, orig_points):
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

    if r != -1:
        print_points(points)
        print(f"R = {r} <= {eps}")
    else:
        cur_eps = max(abs(np.array(points)[:, 1] - np.array(orig_points)[:, 1]))
        while cur_eps > eps:
            h /= 2
            points = method(x0, y0, h, xn, eq)
            orig_points = [(x, orig(x, c)) for x in np.arange(x0, xn + 1e-9, h)]
            cur_eps = max(abs(np.array(points)[:, 1] - np.array(orig_points)[:, 1]))
        print_points(points)
        print(f"eps = {cur_eps} <= {eps}")
    print()
    plt.plot(np.array(points)[:, 0], np.array(points)[:, 1], label=method)
    return points


print("Истинное решение")
print("y =", eq.orig_str(c))
orig_points = [(x, orig(x, c)) for x in np.arange(x0, xn + 1e-9, h)]
print_points(orig_points)
print()
orig_graph_points = [(x, orig(x, c)) for x in np.arange(x0, xn + 1e-6, h / 100)]
plt.plot(np.array(orig_graph_points)[:, 0], np.array(orig_graph_points)[:, 1], label=eq.orig_str(c))

try:
    for method in methods:
        solve(x0, y0, h, xn, eq, method, plt, orig_points)
except Exception as e:
    print("Не получилось решить ОДУ. Вероятно, функция не определена в некоторых точках.")
    plt.ylim(-10, 10)

plt.legend()
plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')
plt.grid()
plt.show()
