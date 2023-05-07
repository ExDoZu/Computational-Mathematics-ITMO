import math
import utils


def lagrange(points, x):
    """Многочлен Лагранжа"""

    def lagrange_coefficient(points, x, index):
        n = len(points) - 1
        p_top = 1
        p_bottom = 1
        for j in range(n + 1):
            if j != index:
                p_top *= (x - points[j][0])
                p_bottom *= (points[index][0] - points[j][0])
        return p_top / p_bottom

    n = len(points) - 1
    summ = 0
    for i in range(n + 1):
        summ += points[i][1] * lagrange_coefficient(points, x, i)
    return summ


def newton(points, x, max_k=None, base_index=0):
    """Интерполяционный многочлен Ньютона с разделенными разностями"""

    def divided_difference(points, i, k, table):
        if k == 0:
            table[i][0] = points[i][1]
            return points[i][1]
        if table[i + 1][k - 1] is None:
            table[i + 1][k - 1] = divided_difference(points, i + 1, k - 1, table)
        if table[i][k - 1] is None:
            table[i][k - 1] = divided_difference(points, i, k - 1, table)
        return (table[i + 1][k - 1] - table[i][k - 1]) / (points[i + k][0] - points[i][0])

    divided_differences = [[None for _ in range(len(points))] for _ in range(len(points))]
    points = points[base_index:len(points)]
    n = len(points) - 1
    if max_k is not None and max_k < n:
        n = max_k
    summ = points[0][1]
    p = 1
    for k in range(1, n + 1):
        p *= (x - points[k - 1][0])
        ds = divided_difference(points, 0, k, divided_differences)
        summ += ds * p
    return summ


def _finite_difference(points, index, power, table):
    if power == 0:
        table[index][power] = points[index][1]
    else:
        if table[index + 1][power - 1] is None:
            table[index + 1][power - 1] = _finite_difference(points, index + 1, power - 1, table)
        if table[index][power - 1] is None:
            table[index][power - 1] = _finite_difference(points, index, power - 1, table)
        table[index][power] = table[index + 1][power - 1] - table[index][power - 1]
    return table[index][power]


def first_newton(points, x, calc_base_index=False) -> (float, list[list[float]]):
    """Первая интерполяционная формула Ньютона для интерполирования вперед"""
    base_index = 0
    if calc_base_index:
        for i in range(len(points)):
            if points[i][0] > x:
                base_index = i - 1
                break
    t = (x - points[base_index][0]) / utils.step(points)
    finite_difference_table = [[None for _ in range(len(points))] for _ in range(len(points))]
    summ = points[base_index][1]
    top_t = 1
    for i in range(1, len(points) - base_index):  #
        top_t *= (t - i + 1)
        summ += _finite_difference(points, base_index, i, finite_difference_table) * top_t / math.factorial(i)
    return summ, finite_difference_table


def second_newton(points, x) -> (float, list[list[float]]):
    """Вторая интерполяционная формула Ньютона для интерполирования назад"""
    n = len(points) - 1
    t = (x - points[n][0]) / utils.step(points)
    finite_difference_table = [[None for _ in range(n + 1)] for _ in range(n + 1)]
    summ = points[n][1]
    top_t = 1
    for i in range(1, n + 1):
        top_t *= (t + i - 1)
        summ += _finite_difference(points, n - i, i, finite_difference_table) * top_t / math.factorial(i)
    return summ, finite_difference_table


def fixed_combined_newton(points, x, calc_base_index=False) -> (float, list[list[float]]):
    """Интерполяциия Ньютона для равноотстоящих узлов"""
    if x <= (points[0][0] + points[-1][0]) / 2:
        return first_newton(points, x, calc_base_index)
    else:
        return second_newton(points, x)


def first_gauss(points, x):
    """Первая интерполяционная формула Гаусса (𝒙 > 𝒂)"""
    if len(points) % 2 == 0:
        raise Exception("Number of points must be odd")
    _2n = len(points) - 1
    index = len(points) // 2
    a = points[index][0]
    t = (x - a) / utils.step(points)
    finite_difference_table = [[None for _ in range(len(points))] for _ in range(len(points))]
    summ = points[index][1]
    top_t = 1
    for i in range(1, _2n + 1):
        if i % 2 == 0:
            top_t *= (t - i // 2)
            index -= 1
        else:
            top_t *= (t + i // 2)
        summ += _finite_difference(points, index, i, finite_difference_table) * top_t / math.factorial(i)
    return summ, finite_difference_table


def second_gauss(points, x):
    """Вторая интерполяционная формула Гаусса (𝒙 < 𝒂)"""
    if len(points) % 2 == 0:
        raise Exception("Number of points must be odd")
    _2n = len(points) - 1
    index = len(points) // 2
    t = (x - points[index][0]) / utils.step(points)
    finite_difference_table = [[None for _ in range(len(points))] for _ in range(len(points))]
    summ = points[index][1]
    top_t = 1
    for i in range(1, _2n + 1):
        if i % 2 == 0:
            top_t *= (t + i // 2)
        else:
            top_t *= (t - i // 2)
            index -= 1
        summ += _finite_difference(points, index, i, finite_difference_table) * top_t / math.factorial(i)
    return summ, finite_difference_table


def combined_gauss(points, x):
    """Интерполирование формулами Гаусса"""
    if x >= (points[0][0] + points[-1][0]) / 2:
        return first_gauss(points, x)
    else:
        return second_gauss(points, x)


def stirling(points, x):
    """Интерполяционный многочлен Стирлинга"""
    if len(points) % 2 == 0:
        raise Exception("Stirling interpolation requires odd number of points")
    _2n = len(points) - 1
    index = len(points) // 2
    t = (x - points[index][0]) / utils.step(points)
    finite_difference_table = [[None for _ in range(len(points))] for _ in range(len(points))]
    summ = points[index][1]
    top_t = 1
    for i in range(1, _2n + 1, 2):
        first_fd = _finite_difference(points, index, i, finite_difference_table)
        second_fd = _finite_difference(points, index - 1, i, finite_difference_table)
        third_fd = _finite_difference(points, index - 1, i + 1, finite_difference_table)
        top_t *= (t ** 2 - (i // 2) ** 2)
        first_summand = top_t / t / math.factorial(i) * (first_fd + second_fd) / 2
        second_summand = top_t / math.factorial(i + 1) * third_fd
        summ += first_summand + second_summand
        index -= 1
    return summ, finite_difference_table


def bessel(points, x):
    """Интерполяционный многочлен Бесселя"""
    if len(points) % 2 != 0:
        raise Exception("Number of points must be even")
    _2n = len(points) - 1
    index = len(points) // 2 - 1
    t = (x - points[index][0]) / utils.step(points)
    finite_difference_table = [[None for _ in range(len(points))] for _ in range(len(points))]
    th = (t - 0.5)
    summ = (points[index][1] + points[index + 1][1]) / 2 + th * _finite_difference(points, index, 1,
                                                                                   finite_difference_table)
    top_t = 1
    for i in range(2, _2n + 1, 2):
        top_t *= (t - i // 2) * (t + i // 2 - 1)
        first_summand = top_t / math.factorial(i) * \
                        (_finite_difference(points, index, i, finite_difference_table) +
                         _finite_difference(points, index - 1, i, finite_difference_table)) / 2
        second_summand = th * top_t / math.factorial(i + 1) * \
                         _finite_difference(points, index - 1, i + 1, finite_difference_table)
        summ += first_summand + second_summand
        index -= 1
    return summ, finite_difference_table
