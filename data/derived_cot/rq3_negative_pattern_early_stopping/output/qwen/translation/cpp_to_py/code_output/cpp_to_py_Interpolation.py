class Interpolation:
    @staticmethod
    def interpolate_1d(x, y, x_interp):
        y_interp = []
        for xi in x_interp:
            found = False
            for i in range(len(x) - 1):
                if x[i] <= xi <= x[i+1]:
                    yi = y[i] + (y[i+1] - y[i]) * (xi - x[i]) / (x[i+1] - x[i])
                    y_interp.append(yi)
                    found = True
                    break
            # If xi is out of bounds, do not append anything
        return y_interp

    @staticmethod
    def interpolate_2d(x, y, z, x_interp, y_interp):
        z_interp = []
        for k in range(len(x_interp)):
            xi = x_interp[k]
            yi = y_interp[k]
            found_x = False
            for i in range(len(x) - 1):
                if x[i] <= xi <= x[i+1]:
                    found_x = True
                    for j in range(len(y) - 1):
                        if y[j] <= yi <= y[j+1]:
                            z00 = z[i][j]
                            z01 = z[i][j+1]
                            z10 = z[i+1][j]
                            z11 = z[i+1][j+1]
                            dx = x[i+1] - x[i]
                            dy = y[j+1] - y[j]
                            zi = (z00 * (x[i+1] - xi) * (y[j+1] - yi) +
                                  z10 * (xi - x[i]) * (y[j+1] - yi) +
                                  z01 * (x[i+1] - xi) * (yi - y[j]) +
                                  z11 * (xi - x[i]) * (yi - y[j])) / (dx * dy)
                            z_interp.append(zi)
                            found_x = True  # Break inner loop
                            break
                    if found_x:
                        break
            # If xi or yi is out of bounds, do not append anything
        return z_interp