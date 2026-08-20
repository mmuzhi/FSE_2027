import math


def _div(dividend, divisor):
    """Division with Java double semantics: dividing by zero yields NaN
    (for 0/0 or NaN/0) or a signed Infinity instead of raising
    ZeroDivisionError."""
    if divisor != 0:
        return dividend / divisor
    if math.isnan(dividend) or dividend == 0:
        return float("nan")
    return math.copysign(float("inf"), dividend * math.copysign(1.0, divisor))


def interpolate1d(x, y, x_interp):
    y_interp = []
    for xi in x_interp:
        for i in range(len(x) - 1):
            if x[i] <= xi <= x[i + 1]:
                yi = y[i] + _div(
                    (y[i + 1] - y[i]) * (xi - x[i]), x[i + 1] - x[i]
                )
                y_interp.append(yi)
                break
    return y_interp


def interpolate2d(x, y, z, x_interp, y_interp):
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
                        zi = _div(
                            z00 * (x[i + 1] - xi) * (y[j + 1] - yi)
                            + z10 * (xi - x[i]) * (y[j + 1] - yi)
                            + z01 * (x[i + 1] - xi) * (yi - y[j])
                            + z11 * (xi - x[i]) * (yi - y[j]),
                            (x[i + 1] - x[i]) * (y[j + 1] - y[j]),
                        )
                        z_interp.append(zi)
                        break
                break
    return z_interp