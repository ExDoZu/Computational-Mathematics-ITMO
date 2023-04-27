from functions import *
from utils import *
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd


def solve_polynom(points: list, power: int):
    xs = [0] * (power * 2 + 1)
    for m in range(power * 2 + 1):
        for x, y in points:
            xs[m] += x ** m

    coef_matrix = []
    for i in range(power + 1):
        coef_matrix.append(xs[i: i + power + 1])

    free_matrix = [0] * (power + 1)
    for m in range(power + 1):
        for x, y in points:
            free_matrix[m] += x ** m * y

    return list(np.linalg.solve(coef_matrix, free_matrix))


def solve_log(points: list):
    new_points = []
    try:
        for x, y in points:
            new_points.append((math.log(x), y))
    except ValueError:
        print("Аппроксимация логарифмической функцией невозможна")
        return None
    return solve_polynom(new_points, 1)


def solve_pow(points: list):
    new_points = []
    try:
        for x, y in points:
            new_points.append((math.log(x), math.log(y)))
    except ValueError:
        print("Аппроксимация степенной функцией невозможна")
        return None
    params = solve_polynom(new_points, 1)
    params[0] = math.exp(params[0])
    return params


def solve_exp(points: list):
    new_points = []
    try:
        for x, y in points:
            new_points.append((x, math.log(y)))
    except ValueError:
        print("Аппроксимация экспоненциальной функцией невозможна")
        return None
    params = solve_polynom(new_points, 1)
    params[0] = math.exp(params[0])
    return params


def create_frame_line(function: Callable, params: list, points: list):
    if params is None:
        return [None, None, None, None, None, None]
    return params + [None] * (4 - len(params)) + [S(function, params, points),
                                                  standard_deviation(function, params, points)]


def print_func_quality(function: Callable, params: list, points: list, name: str = ""):
    if params is None:
        return
    calculated_ys = [function(x, params) for x, y in points]
    data = [[x for x, y in points],
            [y for x, y in points],
            calculated_ys,
            [calculated_y - y for y, calculated_y in zip([y for x, y in points], calculated_ys)]]
    print(name)
    print(pd.DataFrame(data, index=["X", "Y", "φ(x)", "𝛆"]).to_string())
    print()


points = read_points('points2')

linear_params = solve_polynom(points, 1)
double_params = solve_polynom(points, 2)
triple_params = solve_polynom(points, 3)
log_params = solve_log(points)
pow_params = solve_pow(points)
exp_params = solve_exp(points)

print_func_quality(polynom, linear_params, points, "Линейная")
pc = pearson_coef(points)
print(f"Коэффициент корреляции Пирсона: {pc}")
print_func_quality(polynom, double_params, points, "Полином 2 степени")
print_func_quality(polynom, triple_params, points, "Полином 3 степени")
print_func_quality(log_func, log_params, points, "Логарифмическая")
print_func_quality(pow_func, pow_params, points, "Степенная")
print_func_quality(exp_func, exp_params, points, "Экспоненциальная")

print_data = [create_frame_line(polynom, linear_params, points),
              create_frame_line(polynom, double_params, points),
              create_frame_line(polynom, triple_params, points),
              create_frame_line(log_func, log_params, points),
              create_frame_line(pow_func, pow_params, points),
              create_frame_line(exp_func, exp_params, points)
              ]

frame = pd.DataFrame(print_data, columns=["a0", "a1", "a2", "a3", "S", "σ"], index=["Линейная", "Полином 2 степени",
                                                                                    "Полином 3 степени",
                                                                                    "Логарифмическая",
                                                                                    "Степенная", "Экспоненциальная"])

frame = frame.sort_values(by=["σ"])

print(frame.to_string())
name_of_the_best = frame.index[0]
print(f"Наилучшая аппроксимация: {name_of_the_best}")

start_x = min(points, key=lambda x: x[0])[0] - 10
end_x = max(points, key=lambda x: x[0])[0] + 10

plt.xlim(min(points, key=lambda x: x[0])[0] - 1, max(points, key=lambda x: x[0])[0] + 1)
plt.ylim(min(points, key=lambda x: x[1])[1] - 1, max(points, key=lambda x: x[1])[1] + 1)
x = np.linspace(start_x, end_x, 1000)

liny = [polynom(x, linear_params) for x in x]
plt.plot(x, liny, label="Линейная")
douby = [polynom(x, double_params) for x in x]
plt.plot(x, douby, label="Полином 2 степени")
tripy = [polynom(x, triple_params) for x in x]
plt.plot(x, tripy, label="Полином 3 степени")
if exp_params is not None:
    expy = [exp_func(x, exp_params) for x in x]
    plt.plot(x, expy, label="Экспоненциальная")

px = [x for x in x if x > 0]
if log_params is not None:
    logy = [log_func(x, log_params) for x in px]
    plt.plot(px, logy, label="Логарифмическая")
if pow_params is not None:
    powy = [pow_func(x, pow_params) for x in px]
    plt.plot(px, powy, label="Степенная")

plt.scatter([x for x, y in points], [y for x, y in points], label="Исходные точки")
plt.legend()
plt.show()


def draw_one(function: Callable, params: list, points: list):
    plt.xlim(min(points, key=lambda x: x[0])[0] - 1, max(points, key=lambda x: x[0])[0] + 1)
    plt.ylim(min(points, key=lambda x: x[1])[1] - 1, max(points, key=lambda x: x[1])[1] + 1)
    plt.plot(x, [function(x, params) for x in x])
    plt.scatter([x for x, y in points], [y for x, y in points])
    plt.show()


match name_of_the_best:
    case "Линейная":
        draw_one(polynom, linear_params, points)
    case "Полином 2 степени":
        draw_one(polynom, double_params, points)
    case "Полином 3 степени":
        draw_one(polynom, triple_params, points)
    case "Логарифмическая":
        draw_one(log_func, log_params, points)
    case "Степенная":
        draw_one(pow_func, pow_params, points)
    case "Экспоненциальная":
        draw_one(exp_func, exp_params, points)
    case _:
        print("Нет такой функции")
