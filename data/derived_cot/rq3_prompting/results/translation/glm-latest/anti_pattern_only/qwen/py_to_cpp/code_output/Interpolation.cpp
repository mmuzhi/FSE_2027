#include <algorithm>
#include <cstddef>
#include <stdexcept>
#include <vector>

// This is a class that implements the Linear interpolation operation
// of one-dimensional and two-dimensional data.
class Interpolation {
public:
    Interpolation() = default;

    // Linear interpolation of one-dimensional data.
    // x: the x-coordinates of the data points.
    // y: the y-coordinates of the data points.
    // x_interp: the x-coordinates of the interpolation points.
    // Returns: the y-coordinates of the interpolation points.
    //   interpolate_1d({1, 2, 3}, {1, 2, 3}, {1.5, 2.5}) -> {1.5, 2.5}
    static std::vector<double> interpolate_1d(const std::vector<double>& x,
                                              const std::vector<double>& y,
                                              const std::vector<double>& x_interp) {
        std::vector<double> y_interp;
        for (double xi : x_interp) {
            for (std::size_t i = 0; i + 1 < x.size(); ++i) {
                if (x[i] <= xi && xi <= x[i + 1]) {
                    const double denominator = x[i + 1] - x[i];
                    if (denominator == 0.0) {
                        // Python raises ZeroDivisionError here.
                        throw std::runtime_error("ZeroDivisionError: division by zero");
                    }
                    const double yi =
                        y[i] + (y[i + 1] - y[i]) * (xi - x[i]) / denominator;
                    y_interp.push_back(yi);
                    break;
                }
            }
        }
        return y_interp;
    }

    // Linear interpolation of two-dimensional data.
    // x, y: the x-/y-coordinates of the data points.
    // z: the z-coordinates of the data points (z[i][j] belongs to (x[i], y[j])).
    // x_interp, y_interp: the coordinates of the interpolation points
    //                     (paired element-wise, like Python's zip()).
    // Returns: the z-coordinates of the interpolation points.
    //   interpolate_2d({1, 2, 3}, {1, 2, 3}, {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}},
    //                  {1.5, 2.5}, {1.5, 2.5}) -> {3.0, 7.0}
    static std::vector<double> interpolate_2d(const std::vector<double>& x,
                                              const std::vector<double>& y,
                                              const std::vector<std::vector<double>>& z,
                                              const std::vector<double>& x_interp,
                                              const std::vector<double>& y_interp) {
        std::vector<double> z_interp;
        // zip(x_interp, y_interp) iterates only over the shorter of the two.
        const std::size_t pairs = std::min(x_interp.size(), y_interp.size());
        for (std::size_t k = 0; k < pairs; ++k) {
            const double xi = x_interp[k];
            const double yi = y_interp[k];
            for (std::size_t i = 0; i + 1 < x.size(); ++i) {
                if (x[i] <= xi && xi <= x[i + 1]) {
                    for (std::size_t j = 0; j + 1 < y.size(); ++j) {
                        if (y[j] <= yi && yi <= y[j + 1]) {
                            const double z00 = z[i][j];
                            const double z01 = z[i][j + 1];
                            const double z10 = z[i + 1][j];
                            const double z11 = z[i + 1][j + 1];
                            const double denominator =
                                (x[i + 1] - x[i]) * (y[j + 1] - y[j]);
                            if (denominator == 0.0) {
                                // Python raises ZeroDivisionError here.
                                throw std::runtime_error("ZeroDivisionError: division by zero");
                            }
                            const double zi =
                                (z00 * (x[i + 1] - xi) * (y[j + 1] - yi) +
                                 z10 * (xi - x[i]) * (y[j + 1] - yi) +
                                 z01 * (x[i + 1] - xi) * (yi - y[j]) +
                                 z11 * (xi - x[i]) * (yi - y[j])) /
                                denominator;
                            z_interp.push_back(zi);
                            break;
                        }
                    }
                    break;
                }
            }
        }
        return z_interp;
    }
};