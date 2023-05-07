from methods import *
from utils import *
from functions import *

import matplotlib.pyplot as plt
import numpy as np

file_name = "points4"
input_methods = ["Файл данных", "Функция"]
input_method = choose("метод ввода", input_methods)

match input_method:
    case "Файл данных":
        points = read_points(file_name)
        fun = None
        if len(points) < 2:
            print(f"{len(points)} точек. Должно быть минимум 2")
            exit(1)
    case "Функция":
        fun = choose("функцию", functions)
        a = read_number("Левая граница: ")
        b = read_number("Правая граница: ", lambda x: x > a)
        n = read_number("Количество точек: ", lambda x: x > 1, integer=True)

        stp = (b - a) / (n - 1)
        points = [(a + i * stp, fun(a + i * stp)) for i in range(n)]
    case _:
        raise ValueError("Неверный метод ввода")

print_points(points)

x = read_number("Введите X: ", lambda x: points[0][0] <= x <= points[-1][0])

plt.scatter([point[0] for point in points], [point[1] for point in points], label="Точки")
x_array = np.linspace(points[0][0], points[-1][0], 1000)
if fun is not None:
    y_array_original = [fun(x) for x in x_array]
    plt.plot(x_array, y_array_original, label=fun)

print("\nМетод Лагранжа")
print(lagrange(points, x), end="\n\n")
plt.plot(x_array, [lagrange(points, x) for x in x_array], label="Лагранж")

print("Метод Ньютона")
print(newton(points, x), end="\n\n")
plt.plot(x_array, [newton(points, x) for x in x_array], label="Ньютон")


def print_combined_answer(points, x, method):
    answer, table = method(points, x)
    print("Ответ:", answer)
    print("Таблица конечных разностей:")
    print(make_finite_difference_table(table).to_string(), end="\n\n")


print("Метод Ньютона с фиксированным шагом")
if not is_equidistant(points):
    print("Точки не равноотстоящие, метод не применим", end="\n\n")
else:
    print_combined_answer(points, x, fixed_combined_newton)
    plt.plot(x_array, [fixed_combined_newton(points, x)[0] for x in x_array], label="Ньютон с фиксированным шагом")

print("Метод Гаусса")
if not is_equidistant(points):
    print("Точки не равноотстоящие, метод не применим", end="\n\n")
elif len(points) % 2 == 0:
    print("Четное количество точек, метод не применим", end="\n\n")
else:
    print_combined_answer(points, x, combined_gauss)
    plt.plot(x_array, [combined_gauss(points, x)[0] for x in x_array], label="Гаусс")

print("Метод Стирлинга")
if not is_equidistant(points):
    print("Точки не равноотстоящие, метод не применим", end="\n\n")
elif len(points) % 2 == 0:
    print("Четное количество точек, метод не применим", end="\n\n")
else:
    print_combined_answer(points, x, stirling)
    plt.plot(x_array, [stirling(points, x)[0] for x in x_array], label="Стирлинг")

print("Метод Бесселя")
if not is_equidistant(points):
    print("Точки не равноотстоящие, метод не применим", end="\n\n")
elif len(points) % 2 != 0:
    print("Нечетное количество точек, метод не применим", end="\n\n")
else:
    print_combined_answer(points, x, bessel)
    plt.plot(x_array, [bessel(points, x)[0] for x in x_array], label="Бессель")

plt.legend()
plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')
plt.grid()
plt.show()
