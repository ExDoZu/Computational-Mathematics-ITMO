from typing import Callable
import math


def S(function: Callable, params: list, points: list):
    s = 0
    for x, y in points:
        s += (function(x, params) - y) ** 2
    return s


def pearson_coef(points: list):
    n = len(points)
    x_sum = 0
    y_sum = 0
    xy_sum = 0
    x2_sum = 0
    y2_sum = 0
    for x, y in points:
        x_sum += x
        y_sum += y
        xy_sum += x * y
        x2_sum += x ** 2
        y2_sum += y ** 2
    return (n * xy_sum - x_sum * y_sum) / \
        ((n * x2_sum - x_sum ** 2) * (n * y2_sum - y_sum ** 2)) ** 0.5


def pearson_coef2(points: list):
    xmean = sum([x for x, y in points]) / len(points)
    ymean = sum([y for x, y in points]) / len(points)
    xstd = sum([(x - xmean) ** 2 for x, y in points]) ** 0.5
    ystd = sum([(y - ymean) ** 2 for x, y in points]) ** 0.5
    return sum([(x - xmean) * (y - ymean) for x, y in points]) / (xstd * ystd)


def standard_deviation(function: Callable, params: list, points: list):
    return (S(function, params, points) / len(points)) ** 0.5


def read_points(filename: str):
    points = []
    with open(filename) as file:
        for line in file:
            x, y = line.split()
            points.append((float(x), float(y)))
    return points
