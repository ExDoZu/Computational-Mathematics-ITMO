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

# x0 = 1
# xn = 3
# y0 = -1
# h = 0.3
# eps = 0.001

c = sympy.symbols("c")
c = sympy.solve(orig(x0, c) - y0, c)[0]  # constant

n = int((xn + 1e-9 - x0) / h)
new_xn = x0 + n * h
if new_xn < xn:
    xn = new_xn + h
    print(f"xn изменено на {xn:.6f}, так как длина интервала не кратна шагу", end="\n\n")
else:
    xn = new_xn


def solve(x0: float, y0: float, h: float, xn: float, eps: float, eq: Equation, method: Method, plt, orig_points,
          end_runge_rule: bool):
    print(method)
    points = method(x0, y0, h, xn, eq, None if end_runge_rule else eps)
    if method.single_step:
        if end_runge_rule:
            h_half = h / 2
            points_half = method(x0, y0, h_half, xn, eq, None if end_runge_rule else eps)
            while abs(points[-1][1] - points_half[-1][1]) / (2 ** method.p - 1) > eps:
                points = points_half
                h_half /= 2
                points_half = method(x0, y0, h_half, xn, eq)
            print(f"h = {h_half * 2}")
        else:
            h = points[1][0] - points[0][0]
            print(f"h = {h}")
            points_half = method(x0, y0, h / 2, xn, eq)
        print_points(points)
        print(f"R = {abs(points[-1][1] - points_half[-1][1]) / (2 ** method.p - 1)} <= {eps}")

    else:
        cur_eps = max(abs(np.array(points)[:, 1] - np.array(orig_points)[:, 1]))
        print("Max original eps:", cur_eps)
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

for method in methods:
    try:
        solve(x0, y0, h, xn, eps, eq, method, plt, orig_points, True)
    except Exception as e:
        print(f"Не получилось решить ОДУ.\n"
              f"{method.name} не в состоянии эффективно решить это ОДУ,\n"
              f"либо функция прерывается на заданном интервале.\n")
        print(e)
        plt.ylim(-10, 10)

plt.legend()
plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')
plt.grid()
plt.show()
