import sys

import matplotlib.pyplot as plt
from typing import Callable


def create_graph(x: list[float], y: list[float], color: str, roots: list[float] = None) -> None:
    if roots is None:
        roots = []
    plt.plot(x, y, color=color)
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')
    plt.grid(True)
    plt.scatter(roots, [0 for i in range(len(roots))], color='red')
    plt.show()


def calculate_precision(eps: float, num_of_additional_digits: int = 1) -> int:
    if eps <= 0 or num_of_additional_digits < 0:
        raise ValueError("(ᇂ_Jᇂ )")
    precision: int = 0
    while eps < 1:
        eps *= 10
        precision += 1
    return precision + num_of_additional_digits


def derivative(function: Callable[[float], float], x: float, dx: float = 0.0000001) -> float:
    return (function(x + dx) - function(x)) / dx


def derivative_by_x1(function: Callable[[float, float], float], x1: float, x2: float, dx: float = 0.0000001) -> float:
    return (function(x1 + dx, x2) - function(x1, x2)) / dx


def derivative_by_x2(function: Callable[[float, float], float], x1: float, x2: float, dx: float = 0.0000001) -> float:
    return (function(x1, x2 + dx) - function(x1, x2)) / dx


def func(x: float) -> float:
    return x ** 3 + 4.81 * x ** 2 - 17.37 * x + 5.38


def testfunc(x):
    return x ** 3 - x + 4


intervals_of_roots = [(-10, -5), (0, 1), (1, 3)]


def chord(function: Callable[[float], float], a: float, b: float, eps: float = 0.01) -> float:
    def find_x() -> float:
        return (a * function(b) - b * function(a)) / (function(b) - function(a))

    def print_step() -> None:
        precision = calculate_precision(eps)
        print(f"Step {step}: a = {a:.{precision}f}, b = {b:.{precision}f}, x = {new_xk:.{precision}f}, "
              f"f(a) = {function(a):.{precision}f}, f(b) = {function(b):.{precision}f}, "
              f"f(x) = {function(new_xk):.{precision}f}, |x_k+1 - x_k| = {abs(new_xk - xk):.{precision}f}")

    xk = a
    new_xk = find_x()
    y = function(new_xk)
    step = 0
    print_step()
    while abs(new_xk - xk) > eps:
        step += 1
        if y * a < 0:
            b = new_xk
        else:
            a = new_xk
        xk = new_xk
        new_xk = find_x()
        y = function(new_xk)
        print_step()
    return new_xk


# a - default value for x0
# b - not used
def newton(function: Callable[[float], float], a: float, b: float, eps: float = 0.01) -> float:
    def find_x() -> float:
        return xk - function(xk) / derivative(function, xk)

    def print_step() -> None:
        precision = calculate_precision(eps)
        print(f"Step {step}: x_k = {xk:.{precision}f}, f(x_k) = {function(xk):.{precision}f}, "
              f"f'(x_k) = {derivative(function, xk):.{precision}f}, x_k+1 = {new_xk:.{precision}f}, "
              f"|x_k+1 - x_k| = {abs(new_xk - xk):.{precision}f}")

    xk = a
    new_xk = find_x()
    step = 0
    print_step()
    while abs(new_xk - xk) > eps:
        step += 1
        xk = new_xk
        new_xk = find_x()
        print_step()
    return new_xk


# a - default value for x0
# b - not used
def simple_iteration(function: Callable[[float], float], a: float, b: float, eps: float = 0.01) -> float:
    def find_max_derivative(d: int = 10000):
        max_derivative = 0
        for i in range(d):
            x = a + i * (b - a) / d
            current_derivative = abs(derivative(function, x))
            if current_derivative > max_derivative:
                max_derivative = current_derivative
        return max_derivative

    def find_x() -> float:
        return xk + lam * function(xk)

    def print_step() -> None:
        precision = calculate_precision(eps)
        print(f"Step {step}: x_k = {xk:.{precision}f}, x_k+1 = {new_xk:.{precision}f}, "
              f"f(x_k+1) = {function(new_xk):.{precision}f},  |x_k+1 - x_k| = {abs(new_xk - xk):.{precision}f}")

    lam = -1 / find_max_derivative(int(1 / eps))
    xk = a
    new_xk = find_x()
    step = 0
    print_step()
    while abs(new_xk - xk) > eps:
        step += 1
        xk = new_xk
        new_xk = find_x()
        print_step()
    return new_xk


def bisection(function: Callable[[float], float], a: float, b: float, eps: float = 0.01) -> float:
    def print_step() -> None:
        precision = calculate_precision(eps)
        print(f"Step {step}: a = {a:.{precision}f}, b = {b:.{precision}f}, x = {xk:.{precision}f}, "
              f"f(a) = {function(a):.{precision}f}, f(b) = {function(b):.{precision}f}, "
              f"f(x) = {function(xk):.{precision}f}, |a-b| = {abs(a - b):.{precision}f}")

    xk = (a + b) / 2
    step = 0
    print_step()
    while abs(b - a) > eps:
        step += 1
        if function(a) * function(xk) < 0:
            b = xk
        else:
            a = xk
        xk = (a + b) / 2
        print_step()
    return xk


def secant(function: Callable[[float], float], a: float, b: float, eps: float = 0.01) -> float | None:
    def find_x() -> float:
        return xk - (xk - old_xk) * function(xk) / (function(xk) - function(old_xk))

    def print_step() -> None:
        precision = calculate_precision(eps)
        print(f"Step {step}: x_k-1 = {old_xk:.{precision}f}, x_k = {xk:.{precision}f}, x_k+1 = {new_xk:.{precision}f}, "
              f"f(x_k+1) = {function(new_xk):.{precision}f}, |x_k+1 - x_k| = {abs(new_xk - xk):.{precision}f}")

    old_xk = a
    xk = float(input(f"Введите x1 из интервала: ({a}, {b}): "))
    if xk <= a or xk >= b:
        print("Число не из интервала")
        return None
    new_xk = find_x()
    step = 0
    print_step()
    while abs(new_xk - xk) > eps:
        step += 1
        old_xk = xk
        xk = new_xk
        new_xk = find_x()
        print_step()
    return new_xk


def newton_system(system: list[Callable[[float, float], float]], eps: float = 0.01) -> tuple[float, float]:
    def print_step():
        precision = calculate_precision(eps)
        print(f"--------------- Step {step} ---------------------------\n"
              f"X = ({xs[0]:.{precision}}, {xs[1]:.{precision}})\n"
              f"|x_0^k+1 - x_0^k| = {abs(delta_xs[0]):.{precision}f}\n"
              f"|x_1^k+1 - x_1^k| = {abs(delta_xs[1]):.{precision}f}")

    print("Введите начальное приближение:")
    xs: list[float] = list()
    for i in range(len(system)):
        xs.append(float(input(f"x{i}: ")))
    # make matrix for linear system
    matrix: list[list[float]] = list()
    b: list[float] = list()
    delta_xs: list[float] = [sys.float_info.max, sys.float_info.max]
    step = 0
    print_step()
    while abs(delta_xs[0]) > eps or abs(delta_xs[1]) > eps:
        step += 1
        for fun in system:
            row = list()
            row.append(derivative_by_x1(fun, xs[0], xs[1]))
            row.append(derivative_by_x2(fun, xs[0], xs[1]))
            matrix.append(row)
            b.append(-fun(xs[0], xs[1]))
        coef_a = -matrix[1][0] / matrix[1][1] * matrix[0][1] + matrix[0][0]
        coef_c = -b[1] / matrix[1][1] * matrix[0][1] + b[0]
        delta_xs[0] = coef_c / coef_a
        delta_xs[1] = (b[0] - matrix[0][0] * delta_xs[0]) / matrix[0][1]
        xs[0] += delta_xs[0]
        xs[1] += delta_xs[1]
        print_step()
        matrix.clear()
        b.clear()

    return xs[0], xs[1]


def system1() -> list[Callable[[float, float], float]]:
    def f1(x1: float, x2: float) -> float:
        return x1 ** 2 + x2 ** 2 - 4

    def f2(x1: float, x2: float) -> float:
        return -3 * x1 ** 2 + x2

    return [f1, f2]

