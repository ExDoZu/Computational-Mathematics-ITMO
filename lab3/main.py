from functions import *
from methods import *
from utils import *


def calculate_with_runge_rule(method: Method, function: Function, a: float, b: float, eps: float, n: int = 4,
                              printInfo: bool = False):
    s1 = method(function, a, b, n)
    while True:
        n *= 2
        s2 = method(function, a, b, n)
        if abs(s1 - s2) <= eps:
            if printInfo:
                print(f'N = {n}')
            return s2
        s1 = s2


if __name__ == '__main__':
    function = choose("функцию", functions)
    a = read_number("Введите нижний предел интегрирования: ")
    b = read_number("Введите верхний предел интегрирования: ", lambda x: x > a)
    if a <= 0 <= b and function.text == "1/x":
        print("Интеграл не существует")
        exit(0)
    method = choose("метод", methods)
    precision = read_number("Введите точность: ", lambda x: x > 0)
    result = calculate_with_runge_rule(method, function, a, b, precision, printInfo=True)
    print(f"Результат: {result}")
