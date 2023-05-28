import pandas as pd
from typing import Callable


def find_root(function: Callable[[float], float], a: float, b: float, eps: float = 0.01) -> float:
    best_x = a
    best_y = function(a)
    while a <= b:
        abs_y = abs(function(a))
        if abs_y < best_y:
            best_x = a
            best_y = abs_y
        a += eps
    return best_x


def print_points(points):
    print(pd.DataFrame(list(zip(*points)), index=["X", "Y"]).to_string())


def step(points):
    return (points[-1][0] - points[0][0]) / (len(points) - 1)


def read_number(prompt: str, condition: Callable[[any], bool] = lambda x: True, integer: bool = False):
    while True:
        try:
            if (integer):
                value = int(input(prompt))
            else:
                value = float(input(prompt))
            if condition(value):
                return value
            else:
                raise ValueError("Condition not met")
        except ValueError:
            print("Неверный ввод")


def choose(what: str, objects: list):
    choice = read_number(f"Выберите {what}:\n" +
                         "\n".join([f"{i + 1}. {obj}" for i, obj in enumerate(objects)]) + "\n",
                         condition=lambda x: 1 <= x <= len(objects),
                         integer=True)
    print("Выбрано:", objects[choice - 1])
    return objects[choice - 1]
