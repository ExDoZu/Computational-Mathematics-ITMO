from methods import *
from test_functions import *


def my_function(x: float) -> float:
    return x ** 3 + 4.81 * x ** 2 - 17.37 * x + 5.38


# intervals_of_roots = [(-10, -5), (0, 1), (1, 3)]

def input_interval() -> tuple[float, float]:
    a = float(input("Левая граница интервала: "))
    b = float(input("Правая граница интервала: "))
    if a >= b:
        raise ("Невозожный интервал")
    return a, b


def task1():
    x, y = calculate_graph(my_function, -20, 6)
    create_graph(x, y, (-10, 3), "blue")
    print("Левый корень. Метод хорд.")
    a, b = input_interval()
    chord(my_function, a, b)
    print("\nЦентральный корень. Метод Ньютона.")
    a, b = input_interval()
    newton(my_function, a, b)
    print("\nПравый корень. Метод простых итераций.")
    a, b = input_interval()
    simple_iteration(my_function, a, b)


def task2(function: Callable[[float], float]):
    eps = float(input("Введите точность: "))
    precision = calculate_precision(eps, 0)
    a, b = input_interval()
    roots_intervals = find_roots_intervals(function, a, b, eps=eps * 10)
    print(f"Найдено {len(roots_intervals)} интервалов с корнями на ({a:.{precision}f}, {b:.{precision}f}):")
    for interval in roots_intervals:
        print(f"({interval[0]:.{precision}f}, {interval[1]:.{precision}f})")
    x, y = calculate_graph(function, a - abs(b - a), b + abs(b - a))
    create_graph(x, y, (a, b), "blue")
    if len(roots_intervals) == 0:
        return
    print("Введите интервал для уточнения корня")
    la, lb = input_interval()
    choice = int(input("Выберите метод:\n"
                       "1 - метод половинного деления\n"
                       "2 - метод секущих\n"
                       "3 - метод простой итерации\n"))
    match choice:
        case 1:
            bisection(function, la, lb, eps=eps)
        case 2:
            secant(function, la, lb, eps=eps)
        case 3:
            simple_iteration(function, la, lb, eps=eps)
        case _:
            print("Введено что-то не то.")
    create_graph(x, y, (a, b), "blue")


def task3(system: Callable[[], list[Callable[[float, float], float]]]):
    eps = float(input("Введите точность: "))
    a, b = input_interval()

    x1, y1 = calculate_graph2(system()[0], a - (b - a), b + (b - a), (b - a) / 200)
    x2, y2 = calculate_graph2(system()[1], a - (b - a), b + (b - a), (b - a) / 200)

    create_graph2(x1, y1, x2, y2, (a, b), "blue", "red")
    newton_system(system(), eps)
    create_graph2(x1, y1, x2, y2, (a, b), "blue", "red")


def main():
    choice = int(input("Выберите задание:\n"
                       "1 - вычислительная задача\n"
                       "2 - программная задача. Нелинейное уравнение\n"
                       "3 - программная задача. Система нелинейных уравнений\n"))
    match choice:
        case 1:
            task1()
        case 2:
            task2(my_function)
        case 3:
            task3(system2)
        case _:
            print("Введено что-то не то.")


if __name__ == '__main__':
    main()
