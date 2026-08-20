import math


def _ieee_div(a, b):
    # C++ double division follows IEEE 754: dividing by zero yields
    # inf/nan rather than raising an exception like Python's `/`.
    if b == 0.0:
        if a != a or a == 0.0:  # NaN numerator or 0/0 -> NaN
            return float('nan')
        return math.copysign(float('inf'),
                             math.copysign(1.0, a) * math.copysign(1.0, b))
    return a / b


class Interpolation:

    def __init__(self):
        pass

    @staticmethod
    def interpolate_1d(x, y, x_interp):
        y_interp = []
        for xi in x_interp:
            for i in range(len(x) - 1):
                if x[i] <= xi <= x[i + 1]:
                    yi = y[i] + _ieee_div((y[i + 1] - y[i]) * (xi - x[i]),
                                          x[i + 1] - x[i])
                    y_interp.append(yi)
                    break
        return y_interp

    @staticmethod
    def interpolate_2d(x, y, z, x_interp, y_interp):
        z_interp = []
        for k in range(len(x_interp)):
            xi = x_interp[k]
            yi = y_interp[k]
            for i in range(len(x) - 1):
                if x[i] <= xi <= x[i + 1]:
                    for j in range(len(y) - 1):
                        if y[j] <= yi <= y[j + 1]:
                            z00 = z[i][j]
                            z01 = z[i][j + 1]
                            z10 = z[i + 1][j]
                            z11 = z[i + 1][j + 1]
                            zi = _ieee_div(
                                z00 * (x[i + 1] - xi) * (y[j + 1] - yi) +
                                z10 * (xi - x[i]) * (y[j + 1] - yi) +
                                z01 * (x[i + 1] - xi) * (yi - y[j]) +
                                z11 * (xi - x[i]) * (yi - y[j]),
                                (x[i + 1] - x[i]) * (y[j + 1] - y[j]))
                            z_interp.append(zi)
                            break
                    break
        return z_interp