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
    if function == my_function:
        x, y = calculate_graph(function, -12, 5)
        a, b = -10, 3
    elif function == fun2:
        x, y = calculate_graph(function, -10, 5)
        a, b = -6, 3
    elif function == fun3:
        x, y = calculate_graph(function, -20, 20)
        a, b = -10, 10
    else:
        print("Введено что-то не то.")
        return
    create_graph(x, y, (a, b), "blue")
    eps = float(input("Введите точность: "))
    precision = calculate_precision(eps, 0)
    roots_intervals = find_roots_intervals(function, a, b, eps=eps * 10)
    print(f"Найдено {len(roots_intervals)} интервалов с корнями:")
    for interval in roots_intervals:
        print(f"({interval[0]:.{precision}f}, {interval[1]:.{precision}f})")
    if len(roots_intervals) == 0:
        return
    while True:
        print("Введите интервал для уточнения корня")
        la, lb = input_interval()
        if la > lb:
            print("Невозможный интервал")
            return
        flag = False
        count = 0
        for interval in roots_intervals:
            if (interval[0] <= la <= interval[1]) or (interval[0] <= lb <= interval[1]) \
                    or (la <= interval[0] and lb >= interval[1]):
                flag = True
                count += 1
        if flag:
            if count > 1:
                print("В этом интервале может быть несколько корней. Выберите один.")
            else:
                break
        else:
            print("В этом интервале нет корней.")
        for interval in roots_intervals:
            print(f"({interval[0]:.{precision}f}, {interval[1]:.{precision}f})")

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
            return

    create_graph(x, y, (la, lb), "blue")


def task3(system: Callable[[], list[Callable[[float, float], float]]]):
    eps = float(input("Введите точность: "))
    if system == system1:
        a, b = -4, 4
    elif system == system2:
        a, b = -4, 4
    else:
        print("Введено что-то не то.")
        return
    x1, y1 = calculate_graph2(system()[0], a - (b - a), b + (b - a), (b - a) / 200)
    x2, y2 = calculate_graph2(system()[1], a - (b - a), b + (b - a), (b - a) / 200)
    create_graph2(x1, y1, x2, y2, (a, b), "blue", "red")
    newton_system(system(), eps)


def main():
    choice = int(input("Выберите задание:\n"
                       "1 - вычислительная задача\n"
                       "2 - программная задача. Нелинейное уравнение\n"
                       "3 - программная задача. Система нелинейных уравнений\n"))
    match choice:
        case 1:
            task1()
        case 2:
            choice_eq = int(input("Выберите уравнение:\n"
                                  "1 - x^3 + 4.81x^2 - 17.37x + 5.38\n"
                                  "2 - e^x - 2x - 10\n"
                                  "3 - sin(x) - x\n"))

            match choice_eq:
                case 1:
                    chosen_function = my_function
                case 2:
                    chosen_function = fun2
                case 3:
                    chosen_function = fun3
                case _:
                    print("Введено что-то не то.")
                    return
            task2(chosen_function)
        case 3:
            choice_sys = int(input("Выберите систему:\n"
                                   "1) x1^2 + x2^ 2 - 4 = 0\n"
                                   "   -3 * x1^2 + x2 = 0\n"
                                   "2) sin(x1 * x2) = 0\n"
                                   "   tan(x1) + cos(x2) = 0\n"))
            match choice_sys:
                case 1:
                    chosen_system = system1
                case 2:
                    chosen_system = system2
                case _:
                    print("Введено что-то не то.")
                    return
            task3(chosen_system)
        case _:
            print("Введено что-то не то.")


if __name__ == '__main__':
    main()
