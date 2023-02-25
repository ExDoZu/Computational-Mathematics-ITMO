from utils import *
from methods import *
from test_functions import *


def myfunc_var13(x: float) -> float:
    return x ** 3 + 4.81 * x ** 2 - 17.37 * x + 5.38


# intervals_of_roots = [(-10, -5), (0, 1), (1, 3)]


def task1():
    x, y = calculate_graph(myfunc_var13, -10, 3)
    create_graph(x, y, "blue")
    print("Левый корень. Метод хорд.")
    a = float(input("Левая граница итервала: "))
    b = float(input("Правая граница интервала: "))
    chord(myfunc_var13, a, b)
    print("\nЦентральный корень. Метод Ньютона.")
    a = float(input("Левая граница итервала: "))
    b = float(input("Правая граница интервала: "))
    newton(myfunc_var13, a, b)
    print("\nПравый корень. Метод простых итераций.")
    a = float(input("Левая граница итервала: "))
    b = float(input("Правая граница интервала: "))
    simple_iteration(myfunc_var13, a, b)


def task2():
    ...


def task3():
    ...


choice = int(input("Выберите задание:\n"
                   "1 - вычислительная задача\n"
                   "2 - программная задача. Нелинейное уравнение\n"
                   "3 - программная задача. Система нелинейных уравнений\n"))
match choice:
    case 1:
        task1()
    case 2:
        task2()
    case 3:
        task3()
    case _:
        print("Введено что-то не то.")

# x1, y1 = calculate_graph2(system2()[0], -3, 3)
# x2, y2 = calculate_graph2(system2()[1], -3, 3)
# create_graph2(x1, y1, x2, y2, "blue", "red")
# newton_system(system2())
# create_graph2(x1, y1, x2, y2, "blue", "red")
