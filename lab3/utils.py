from typing import Callable


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
