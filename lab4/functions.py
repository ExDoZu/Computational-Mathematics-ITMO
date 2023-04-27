import math


def polynom(x: float, params: list[float]):
    result = 0
    for i, param in enumerate(params):
        result += param * x ** i
    return result


def log_func(x: float, params: list[float]):
    if len(params) != 2:
        raise ValueError("params must be of length 2")
    if x <= 0:
        raise ValueError("x must be positive")
    return params[1] * math.log(x) + params[0]


def pow_func(x: float, params: list[float]):
    if len(params) != 2:
        raise ValueError("params must be of length 2")
    if x <= 0:
        raise ValueError("x must be positive")
    return params[0] * x ** params[1]


def exp_func(x: float, params: list[float]):
    if len(params) != 2:
        raise ValueError("params must be of length 2")
    return params[0] * math.exp(params[1] * x)
