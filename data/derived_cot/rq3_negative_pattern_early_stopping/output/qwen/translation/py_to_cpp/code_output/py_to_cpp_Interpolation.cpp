#include <vector>
#include <utility> // For std::pair

class Interpolation {
public:
    static std::vector<double> interpolate_1d(const std::vector<double>& x, const std::vector<double>& y, const std::vector<double>& x_interp) {
        std::vector<double> y_interp;
        for (double xi : x_interp) {
            bool found = false;
            for (size_t i = 0; i < x.size() - 1; ++i) {
                if (x[i] <= xi && xi <= x[i+1]) {
                    double yi = y[i] + (y[i+1] - y[i]) * (xi - x[i]) / (x[i+1] - x[i]);
                    y_interp.push_back(yi);
                    found = true;
                    break;
                }
            }
            // If not found, do nothing (skip this interpolation point)
        }
        return y_interp;
    }

    static std::vector<double> interpolate_2d(const std::vector<double>& x, const std::vector<double>& y, const std::vector<std::vector<double>>& z, const std::vector<double>& x_interp, const std::vector<double>& y_interp) {
        std::vector<double> z_interp;
        for (size_t i = 0; i < x_interp.size(); ++i) {
            double xi = x_interp[i];
            double yi = y_interp[i];
            bool x_found = false;
            for (size_t a = 0; a < x.size() - 1; ++a) {
                if (x[a] <= xi && xi <= x[a+1]) {
                    x_found = true;
                    for (size_t b = 0; b < y.size() - 1; ++b) {
                        if (y[b] <= yi && yi <= y[b+1]) {
                            double z00 = z[a][b];
                            double z01 = z[a][b+1];
                            double z10 = z[a+1][b];
                            double z11 = z[a+1][b+1];
                            double denom = (x[a+1] - x[a]) * (y[b+1] - y[b]);
                            double numerator = (
                                z00 * (x[a+1] - xi) * (y[b+1] - yi) +
                                z10 * (xi - x[a]) * (y[b+1] - yi) +
                                z01 * (x[a+1] - xi) * (yi - y[b]) +
                                z11 * (xi - x[a]) * (yi - y[b])
                            );
                            double zi = numerator / denom;
                            z_interp.push_back(zi);
                            break;
                        }
                    }
                    break;
                }
            }
            // If either x or y not found, skip this interpolation point
        }
        return z_interp;
    }
};