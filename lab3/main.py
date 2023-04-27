from functions import *
from methods import *
from utils import *


def calculate_with_runge_rule(method: Method, function: Function, a: float, b: float, eps: float, n: int = 4,
                              printInfo: bool = False):
    s1 = method(function, a, b, n)
    while True:

        n *= 2
        s2 = method(function, a, b, n)
        if (method.text == "Метод Симпсона"):
            k = 4
        else:
            k = 2
        if printInfo:
            print(f'N = {n}\n'
                  f'k = {k}\n'
                  f'|S1-S2| = {abs(s1 - s2)}\n'
                  f'|S1 - S2| / (2^k - 1) = {abs(s1 - s2) / (2 ** k - 1)}')

        if abs(s1 - s2) / (2 ** k - 1) <= eps:
            if printInfo:
                print(f'N = {n}')
            return s2
        s1 = s2


if __name__ == '__main__':
    function = choose("функцию", functions)
    a = read_number("Введите нижний предел интегрирования: ")
    b = read_number("Введите верхний предел интегрирования: ", lambda x: x > a)
    method = choose("метод", methods)
    precision = read_number("Введите точность: ", lambda x: x > 0)
    result = calculate_with_runge_rule(method, function, a, b, precision, printInfo=True)
    print(f"Результат: {result}")
