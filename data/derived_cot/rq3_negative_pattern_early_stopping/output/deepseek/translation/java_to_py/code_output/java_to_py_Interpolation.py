from typing import List

class Interpolation:
    @staticmethod
    def interpolate1d(x: List[float], y: List[float], x_interp: List[float]) -> List[float]:
        """Perform 1D linear interpolation."""
        y_interp = []
        for xi in x_interp:
            for i in range(len(x) - 1):
                if x[i] <= xi <= x[i + 1]:
                    yi = y[i] + (y[i + 1] - y[i]) * (xi - x[i]) / (x[i + 1] - x[i])
                    y_interp.append(yi)
                    break
        return y_interp

    @staticmethod
    def interpolate2d(
        x: List[float],
        y: List[float],
        z: List[List[float]],
        x_interp: List[float],
        y_interp: List[float]
    ) -> List[float]:
        """Perform 2D bilinear interpolation."""
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
                            zi = (
                                z00 * (x[i + 1] - xi) * (y[j + 1] - yi) +
                                z10 * (xi - x[i]) * (y[j + 1] - yi) +
                                z01 * (x[i + 1] - xi) * (yi - y[j]) +
                                z11 * (xi - x[i]) * (yi - y[j])
                            ) / ((x[i + 1] - x[i]) * (y[j + 1] - y[j]))
                            z_interp.append(zi)
                            break
                    break
        return z_interp