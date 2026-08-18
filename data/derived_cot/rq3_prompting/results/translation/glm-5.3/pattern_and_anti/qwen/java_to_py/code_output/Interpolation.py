def _jdiv(a, b):
    # Mimic Java double division: never raises; 0/0 -> NaN, x/0 -> +/-Inf
    if b != 0.0:
        return a / b
    if a == 0.0:
        return float('nan')
    return float('inf') if a > 0 else float('-inf')


def interpolate1d(x, y, x_interp):
    y_interp = []
    for xi in x_interp:
        for i in range(len(x) - 1):
            if x[i] <= xi <= x[i + 1]:
                yi = y[i] + _jdiv((y[i + 1] - y[i]) * (xi - x[i]), x[i + 1] - x[i])
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
                        num = (z00 * (x[i + 1] - xi) * (y[j + 1] - yi) +
                               z10 * (xi - x[i]) * (y[j + 1] - yi) +
                               z01 * (x[i + 1] - xi) * (yi - y[j]) +
                               z11 * (xi - x[i]) * (yi - y[j]))
                        den = (x[i + 1] - x[i]) * (y[j + 1] - y[j])
                        zi = _jdiv(num, den)
                        z_interp.append(zi)
                        break
                break
    return z_interp