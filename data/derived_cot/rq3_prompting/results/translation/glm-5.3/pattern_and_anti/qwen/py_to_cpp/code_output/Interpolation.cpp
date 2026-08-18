#include <vector>
#include <cstddef>

class Interpolation {
public:
    Interpolation() {}

    // Linear interpolation of one-dimensional data
    // x: x-coordinates of data points
    // y: y-coordinates of data points
    // x_interp: x-coordinates of interpolation points
    // Returns: y-coordinates of interpolation points
    static std::vector<double> interpolate_1d(const std::vector<double>& x,
                                              const std::vector<double>& y,
                                              const std::vector<double>& x_interp) {
        std::vector<double> y_interp;
        for (double xi : x_interp) {
            for (size_t i = 0; i + 1 < x.size(); ++i) {
                if (x[i] <= xi && xi <= x[i + 1]) {
                    double yi = y[i] + (y[i + 1] - y[i]) * (xi - x[i]) / (x[i + 1] - x[i]);
                    y_interp.push_back(yi);
                    break;
                }
            }
        }
        return y_interp;
    }

    // Linear interpolation of two-dimensional data
    // x: x-coordinates of data points
    // y: y-coordinates of data points
    // z: z-coordinates of data points (2D grid)
    // x_interp: x-coordinates of interpolation points
    // y_interp: y-coordinates of interpolation points
    // Returns: z-coordinates of interpolation points
    static std::vector<double> interpolate_2d(const std::vector<double>& x,
                                              const std::vector<double>& y,
                                              const std::vector<std::vector<double>>& z,
                                              const std::vector<double>& x_interp,
                                              const std::vector<double>& y_interp) {
        std::vector<double> z_interp;
        // zip(x_interp, y_interp): stop at the shorter of the two
        size_t n = x_interp.size() < y_interp.size() ? x_interp.size() : y_interp.size();
        for (size_t k = 0; k < n; ++k) {
            double xi = x_interp[k];
            double yi = y_interp[k];
            for (size_t i = 0; i + 1 < x.size(); ++i) {
                if (x[i] <= xi && xi <= x[i + 1]) {
                    for (size_t j = 0; j + 1 < y.size(); ++j) {
                        if (y[j] <= yi && yi <= y[j + 1]) {
                            double z00 = z[i][j];
                            double z01 = z[i][j + 1];
                            double z10 = z[i + 1][j];
                            double z11 = z[i + 1][j + 1];
                            double zi = (z00 * (x[i + 1] - xi) * (y[j + 1] - yi) +
                                         z10 * (xi - x[i]) * (y[j + 1] - yi) +
                                         z01 * (x[i + 1] - xi) * (yi - y[j]) +
                                         z11 * (xi - x[i]) * (yi - y[j])) /
                                        ((x[i + 1] - x[i]) * (y[j + 1] - y[j]));
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