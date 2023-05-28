from typing import Callable


class Method:
    def __init__(self, method: Callable[
        [float, float, float, float, Callable[[float, float], float]], list[tuple[float, float]]], name: str):
        self.method = method
        self.name = name

    def __call__(self, x0: float,
                 y0: float,
                 h: float,
                 xn: float,
                 derivative: Callable[[float, float], float]) -> list[tuple[float, float]]:
        return self.method(x0, y0, h, xn, derivative)

    def __str__(self):
        return self.name


def euler(x0: float,
          y0: float,
          h: float,
          xn: float,
          derivative: Callable[[float, float], float]) -> list[tuple[float, float]]:
    result = [(x0, y0)]
    n = int((xn - x0) / h)
    for i in range(n):
        x = result[-1][0]
        y = result[-1][1]
        result.append((x + h, y + h * derivative(x, y)))
    return result


def mod_euler(x0: float,
              y0: float,
              h: float,
              xn: float,
              derivative: Callable[[float, float], float]) -> list[tuple[float, float]]:
    """Метод Рунге – Кутты II порядка"""
    result = [(x0, y0)]
    n = int((xn - x0) / h)
    for i in range(n):
        x = result[-1][0]
        y = result[-1][1]
        k1 = h * derivative(x, y)
        k2 = h * derivative(x + h, y + k1)
        result.append((x + h, y + 0.5 * (k1 + k2)))
    return result


rk2: Callable[[float, float, float, int, Callable[[float, float], float]], list[tuple[float, float]]] = mod_euler


def rk4(x0: float,
        y0: float,
        h: float,
        xn: float,
        derivative: Callable[[float, float], float]) -> list[tuple[float, float]]:
    """Метод Рунге – Кутты VI порядка"""
    result = [(x0, y0)]
    n = int((xn - x0) / h)
    for i in range(n):
        x = result[-1][0]
        y = result[-1][1]
        k1 = h * derivative(x, y)
        k2 = h * derivative(x + h / 2, y + k1 / 2)
        k3 = h * derivative(x + h / 2, y + k2 / 2)
        k4 = h * derivative(x + h, y + k3)
        result.append((x + h, y + 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)))
    return result


def adams(data: list[tuple[float, float]], h: float, xn: float, derivative: Callable[[float, float], float]) \
        -> list[tuple[float, float]]:
    """
    Метод Адамса
    :param data: содержится минимум 4 заранее вычисленных значения.
    """
    result = data.copy()
    n = int((xn - data[-1][0]) / h)
    for i in range(n):
        df = [derivative(x, y) for x, y in result[len(result) - 4:]]
        ddf1 = df[-1] - df[-2]
        ddf2 = ddf1 - df[-2] + df[-3]
        ddf3 = ddf2 - df[-2] + 2 * df[-3] - df[-4]
        x = result[-1][0]
        y = result[-1][1]
        result.append((x + h, y +
                       h * df[-1] +
                       1 / 2 * h ** 2 * ddf1 +
                       5 / 12 * h ** 3 * ddf2 +
                       3 / 8 * h ** 4 * ddf3))
    return result


def milne(data: list[tuple[float, float]], h: float, xn: float, derivative: Callable[[float, float], float],
          precision=1e-6) -> list[tuple[float, float]]:
    """
    Метод Милна
    :param data: содержится минимум 4 заранее вычисленных значения.
    """

    def calc_y_corr():
        return result[-2][1] + h / 3 * (df[-2] + 4 * df[-1] + derivative(result[-1][0] + h, y_pred))

    result = data.copy()
    n = int((xn - data[-1][0]) / h)
    for i in range(n):
        df = [derivative(x, y) for x, y in result[len(result) - 3:]]
        y_pred = result[-4][1] + 4 / 3 * h * (2 * df[-3] - df[-2] + 2 * df[-1])
        y_corr = calc_y_corr()
        while abs(y_pred - y_corr) < precision:
            y_pred = y_corr
            y_corr = calc_y_corr()
        result.append((result[-1][0] + h, y_corr))
    return result


def rk4_milne(x0: float,
              y0: float,
              h: float,
              xn: float,
              derivative: Callable[[float, float], float]) -> list[tuple[float, float]]:
    result = rk4(x0, y0, h, x0 + 3 * h + 1e-9, derivative)
    result = milne(result, h, xn, derivative)
    return result


def rk4_adams(x0: float,
              y0: float,
              h: float,
              xn: float,
              derivative: Callable[[float, float], float]) -> list[tuple[float, float]]:
    result = rk4(x0, y0, h, x0 + 3 * h + 1e-9, derivative)
    result = adams(result, h, xn, derivative)
    return result


methods = [Method(euler, "Метод Эйлера"), Method(mod_euler, "Мод. метод Эйлера"),
           Method(rk4, "Метод Рунге-Кутты 4 порядка"),
           Method(rk4_adams, "Метод Адамса"), Method(rk4_milne, "Метод Милна")]