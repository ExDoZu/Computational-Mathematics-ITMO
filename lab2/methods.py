from utils import *


def chord(function: Callable[[float], float], a: float, b: float, eps: float = 0.01) -> float:
    def find_x() -> float:
        return (a * function(b) - b * function(a)) / (function(b) - function(a))

    def print_step() -> None:
        min_value = min((eps, abs(new_xk), abs(function(a)), abs(function(b)), abs(function(new_xk)), abs(new_xk - xk)),
                        key=lambda x: x if x > 0 else 1)
        precision = calculate_precision(min_value)
        print(f"Step {step}: a = {a:.{precision}f}, b = {b:.{precision}f}, x = {new_xk:.{precision}f}, "
              f"f(a) = {function(a):.{precision}f}, f(b) = {function(b):.{precision}f}, "
              f"f(x) = {function(new_xk):.{precision}f}, |x_k+1 - x_k| = {abs(new_xk - xk):.{precision}f}")

    xk = a
    new_xk = find_x()
    y = function(new_xk)
    step = 0
    print_step()
    while abs(new_xk - xk) > eps:
        step += 1
        if y * a < 0:
            b = new_xk
        else:
            a = new_xk
        xk = new_xk
        new_xk = find_x()
        y = function(new_xk)
        print_step()
    return new_xk


def chord_fixed(function: Callable[[float], float], a: float, b: float, eps: float = 0.01) -> float:
    def print_step() -> None:
        min_value = min((eps, abs(new_xk), abs(a), abs(b), abs(function(a)), abs(function(b)), abs(function(new_xk)),
                         abs(new_xk - xk)), key=lambda x: x if x > 0 else 1)
        precision = calculate_precision(min_value)
        print(f"Step {step}: a = {a:.{precision}f}, b = {b:.{precision}f}, x = {new_xk:.{precision}f}, "
              f"f(a) = {function(a):.{precision}f}, f(b) = {function(b):.{precision}f}, "
              f"f(x) = {function(new_xk):.{precision}f}, |x_k+1 - x_k| = {abs(new_xk - xk):.{precision}f}")

    def find_x_left_fixed() -> float:
        return xk - (a - xk) / (function(a) - function(xk)) * function(xk)

    def find_x_right_fixed() -> float:
        return xk - (b - xk) / (function(b) - function(xk)) * function(xk)

    xk = (a + b) / 2
    if derivative(function, xk) * derivative2(function, xk) > 0:
        print("Правая граница фиксирована")
        find_x = find_x_right_fixed
        xk = a
    else:
        print("Левая граница фиксирована")
        find_x = find_x_left_fixed
        xk = b
    new_xk = find_x()
    step = 0
    print_step()
    while abs(new_xk - xk) > eps:
        step += 1
        xk = new_xk
        new_xk = find_x()
        print_step()
    return new_xk


# a - default value for x0
# b - not used
def newton(function: Callable[[float], float], a: float, b: float, eps: float = 0.01) -> float:
    def find_x() -> float:
        return xk - function(xk) / derivative(function, xk)

    def print_step() -> None:
        min_value = min((eps, abs(new_xk), abs(derivative(function, xk)), abs(xk), abs(function(new_xk)),
                         abs(new_xk - xk)), key=lambda x: x if x > 0 else 1)
        precision = calculate_precision(min_value)
        print(f"Step {step}: x_k = {xk:.{precision}f}, f(x_k) = {function(xk):.{precision}f}, "
              f"f'(x_k) = {derivative(function, xk):.{precision}f}, x_k+1 = {new_xk:.{precision}f}, "
              f"|x_k+1 - x_k| = {abs(new_xk - xk):.{precision}f}")

    xk = a
    new_xk = find_x()
    step = 0
    print_step()
    while abs(new_xk - xk) > eps:
        step += 1
        xk = new_xk
        new_xk = find_x()
        print_step()
    return new_xk


# a - default value for x0
# b - not used
def simple_iteration(function: Callable[[float], float], a: float, b: float, eps: float = 0.01) -> float:
    def find_max_derivative(d: int = 10000):
        max_derivative = 0
        for i in range(d):
            x = a + i * (b - a) / d
            current_derivative = abs(derivative(function, x))
            if current_derivative > max_derivative:
                max_derivative = current_derivative
        return max_derivative

    def find_x() -> float:
        return xk + lam * function(xk)

    def print_step() -> None:
        min_value = min((eps, abs(new_xk), abs(xk), abs(function(new_xk)), abs(new_xk - xk)),
                        key=lambda x: x if x > 0 else 1)
        precision = calculate_precision(min_value)
        print(f"Step {step}: x_k = {xk:.{precision}f}, x_k+1 = {new_xk:.{precision}f}, "
              f"f(x_k+1) = {function(new_xk):.{precision}f},  |x_k+1 - x_k| = {abs(new_xk - xk):.{precision}f}")

    lam = -1 / find_max_derivative(int(1 / eps))

    max_step = float("inf")
    fi = abs(1 + lam * derivative(function, a))
    fi2 = abs(1 + lam * derivative(function, b))
    print(f"|𝜑'({a})| = {fi:.3f}, |𝜑'({b})| = {fi2:.3f}")
    if fi >= 1 or fi2 >= 1:
        print("Метод не должен сходиться на данном интервале.")
        max_step = int(input("Введите максимальное количество итераций: "))
    xk = float(input("Введите начальное приближение x0: "))
    new_xk = find_x()
    step = 0
    print_step()
    while (abs(new_xk - xk) > eps or abs(function(new_xk)) > eps) and step < max_step:
        step += 1
        xk = new_xk
        new_xk = find_x()
        print_step()
    print(f"Ответ: {new_xk}\nf({new_xk}) = {function(new_xk)}\n|x_k+1 - x_k| = {abs(new_xk - xk)}")
    return new_xk


def bisection(function: Callable[[float], float], a: float, b: float, eps: float = 0.01) -> float:
    def print_step() -> None:
        min_value = min((eps, abs(xk), abs(a), abs(b), abs(function(a)), abs(function(b)), abs(function(xk)),
                         abs(a - b)), key=lambda x: x if x > 0 else 1)
        precision = calculate_precision(min_value)
        print(f"Step {step}: a = {a:.{precision}f}, b = {b:.{precision}f}, x = {xk:.{precision}f}, "
              f"f(a) = {function(a):.{precision}f}, f(b) = {function(b):.{precision}f}, "
              f"f(x) = {function(xk):.{precision}f}, |a-b| = {abs(a - b):.{precision}f}")

    while True:
        xk = float(input(f"Введите начальное приближение x0 из отрезка: [{a}, {b}]: "))
        if xk < a or xk > b:
            print("Число не из отрезка")
        else:
            break
    step = 0
    print_step()
    while abs(b - a) > eps or abs(function(xk)) > eps:
        step += 1
        if function(a) * function(xk) < 0:
            b = xk
        else:
            a = xk
        xk = (a + b) / 2
        print_step()
    print(f"Ответ: {xk}\nf({xk}) = {function(xk)}\n|b - a| = {abs(b - a)}")
    return xk


def secant(function: Callable[[float], float], a: float, b: float, eps: float = 0.01) -> float | None:
    def find_x() -> float:
        return xk - (xk - old_xk) * function(xk) / (function(xk) - function(old_xk))

    def print_step() -> None:
        min_value = min((eps, abs(new_xk), abs(xk), abs(old_xk), abs(function(new_xk)), abs(new_xk - xk)),
                        key=lambda x: x if x > 0 else 1)
        precision = calculate_precision(min_value)
        print(f"Step {step}: x_k-1 = {old_xk:.{precision}f}, x_k = {xk:.{precision}f}, x_k+1 = {new_xk:.{precision}f}, "
              f"f(x_k+1) = {function(new_xk):.{precision}f}, |x_k+1 - x_k| = {abs(new_xk - xk):.{precision}f}")

    if function(a) * derivative2(function, a) > 0:
        print(f"x0 = {a}")
        old_xk = a
    elif function(b) * derivative2(function, b) > 0:
        print(f"x0 = {b}")
        old_xk = b
    else:
        print(f"Быстрая сходимость не обеспечивается из точки a = {a} и из точки b = {b}.\n")
        while True:
            old_xk = float(input(f"Введите начальное приближение x0 из интервала: ({a}, {b}): "))
            if old_xk <= a or old_xk >= b:
                print("Число не из интервала")
            else:
                break

    while True:
        xk = float(input(f"Введите начальное приближение x1 из интервала: ({a}, {b}): "))
        if xk < a or xk > b:
            print("Число не из интервала")
        else:
            break
    new_xk = find_x()
    step = 0
    print_step()
    while abs(new_xk - xk) > eps or abs(function(new_xk)) > eps:
        step += 1
        old_xk = xk
        xk = new_xk
        new_xk = find_x()
        print_step()
    print(f"Ответ: {new_xk}\nf({new_xk}) = {function(new_xk)}\n|x_k+1 - x_k| = {abs(new_xk - xk)}")
    return new_xk


def newton_system(system: list[Callable[[float, float], float]], eps: float = .01) -> tuple[float | None, float | None]:
    def print_step():
        min_value = min((eps, abs(xs[0]), abs(xs[1]), abs(delta_xs[0]), abs(delta_xs[1])),
                        key=lambda x: x if x > 0 else 1)
        precision = calculate_precision(min_value)
        print(f"--------------- Step {step} ---------------------------\n"
              f"X = ({xs[0]:.{precision}}, {xs[1]:.{precision}})\n"
              f"|x_0^k+1 - x_0^k| = {delta_xs[0]:.{precision}f}\n"
              f"|x_1^k+1 - x_1^k| = {delta_xs[1]:.{precision}f}")

    print("Введите начальное приближение:")
    xs: list[float] = list()
    for i in range(len(system)):
        xs.append(float(input(f"x{i}: ")))
    # make matrix for linear system
    matrix: list[list[float]] = list()
    b: list[float] = list()
    delta_xs: list[float] = [float("inf"), float("inf")]
    step = 0
    max_step = int(input("Введите максимальное количество шагов: "))

    while (abs(delta_xs[0]) > eps or abs(delta_xs[1]) > eps) and step < max_step:
        step += 1
        for fun in system:
            row = list()
            row.append(derivative_by_x1(fun, xs[0], xs[1], 0.00000001))
            row.append(derivative_by_x2(fun, xs[0], xs[1], 0.00000001))
            matrix.append(row)
            b.append(-fun(xs[0], xs[1]))
        # print(f"--------------- Step {step} ---------------------------\n"
        #       "Matrix:\n"
        #       f"{matrix[0][0]} {matrix[0][1]} | {b[0]}\n"
        #       f"{matrix[1][0]} {matrix[1][1]} | {b[1]}")

        # if matrix[0][1] == 0.0 or matrix[1][1] == 0.0:
        #     print("Ой-ой-ой. Деление на 0")
        #     return None, None
        # coef_a = -matrix[1][0] / matrix[1][1] * matrix[0][1] + matrix[0][0]
        # if coef_a == 0.0:
        #     print("Ой-ой-ой. Деление на 0")
        #     return None, None
        # coef_c = -b[1] / matrix[1][1] * matrix[0][1] + b[0]
        # delta_xs[0] = coef_c / coef_a
        # delta_xs[1] = (b[0] - matrix[0][0] * delta_xs[0]) / matrix[0][1]

        # метод Крамера
        det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        if det == 0.0:
            print(f"--------------- Step {step} ---------------------------\n"
                  "Matrix:\n"
                  f"{matrix[0][0]} {matrix[0][1]} | {b[0]}\n"
                  f"{matrix[1][0]} {matrix[1][1]} | {b[1]}")
            print("Не удалось найти решение. Метод не сходится из заданной точки.")
            return None, None
        delta_xs[0] = (b[0] * matrix[1][1] - b[1] * matrix[0][1]) / det
        delta_xs[1] = (b[1] * matrix[0][0] - b[0] * matrix[1][0]) / det
        xs[0] += delta_xs[0]
        xs[1] += delta_xs[1]
        print_step()
        matrix.clear()
        b.clear()
    print(f"Ответ: ({xs[0]}, {xs[1]})")
    min_value = min((eps, abs(system[0](xs[0], xs[1])), abs(system[1](xs[0], xs[1]))), key=lambda x: x if x > 0 else 1)
    precision = calculate_precision(min_value)
    print(f"f(x, y) = {system[0](xs[0], xs[1]):.{precision}f}\ng(x, y) = {system[1](xs[0], xs[1]):.{precision}f}")
    return xs[0], xs[1]
