from typing import List

def interpolate1d(x: List[float], y: List[float], xInterp: List[float]) -> List[float]:
    yInterp = []
    for xi in xInterp:
        for i in range(len(x) - 1):
            if x[i] <= xi <= x[i + 1]:
                yi = y[i] + (y[i + 1] - y[i]) * (xi - x[i]) / (x[i + 1] - x[i])
                yInterp.append(yi)
                break
    return yInterp


def interpolate2d(
    x: List[float],
    y: List[float],
    z: List[List[float]],
    xInterp: List[float],
    yInterp: List[float],
) -> List[float]:
    zInterp = []
    for k in range(len(xInterp)):
        xi = xInterp[k]
        yi = yInterp[k]
        for i in range(len(x) - 1):
            if x[i] <= xi <= x[i + 1]:
                for j in range(len(y) - 1):
                    if y[j] <= yi <= y[j + 1]:
                        z00 = z[i][j]
                        z01 = z[i][j + 1]
                        z10 = z[i + 1][j]
                        z11 = z[i + 1][j + 1]
                        zi = (
                            z00 * (x[i + 1] - xi) * (y[j + 1] - yi)
                            + z10 * (xi - x[i]) * (y[j + 1] - yi)
                            + z01 * (x[i + 1] - xi) * (yi - y[j])
                            + z11 * (xi - x[i]) * (yi - y[j])
                        ) / ((x[i + 1] - x[i]) * (y[j + 1] - y[j]))
                        zInterp.append(zi)
                        break
                break
    return zInterp