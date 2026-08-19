#pragma once

#include <vector>

namespace org {
namespace example {

class Interpolation {
public:
    static std::vector<double> interpolate1d(const std::vector<double>& x,
                                             const std::vector<double>& y,
                                             const std::vector<double>& xInterp) {
        std::vector<double> yInterp;
        for (double xi : xInterp) {
            // Note: int comparison preserves Java semantics for empty input
            // (size() - 1 would underflow with size_t).
            for (int i = 0; i < static_cast<int>(x.size()) - 1; i++) {
                if (x.at(i) <= xi && xi <= x.at(i + 1)) {
                    double yi = y.at(i) + (y.at(i + 1) - y.at(i)) * (xi - x.at(i)) / (x.at(i + 1) - x.at(i));
                    yInterp.push_back(yi);
                    break;
                }
            }
        }
        return yInterp;
    }

    static std::vector<double> interpolate2d(const std::vector<double>& x,
                                             const std::vector<double>& y,
                                             const std::vector<std::vector<double>>& z,
                                             const std::vector<double>& xInterp,
                                             const std::vector<double>& yInterp) {
        std::vector<double> zInterp;
        for (std::size_t k = 0; k < xInterp.size(); k++) {
            double xi = xInterp.at(k);
            double yi = yInterp.at(k);
            for (int i = 0; i < static_cast<int>(x.size()) - 1; i++) {
                if (x.at(i) <= xi && xi <= x.at(i + 1)) {
                    for (int j = 0; j < static_cast<int>(y.size()) - 1; j++) {
                        if (y.at(j) <= yi && yi <= y.at(j + 1)) {
                            double z00 = z.at(i).at(j);
                            double z01 = z.at(i).at(j + 1);
                            double z10 = z.at(i + 1).at(j);
                            double z11 = z.at(i + 1).at(j + 1);
                            double zi = (z00 * (x.at(i + 1) - xi) * (y.at(j + 1) - yi) +
                                         z10 * (xi - x.at(i)) * (y.at(j + 1) - yi) +
                                         z01 * (x.at(i + 1) - xi) * (yi - y.at(j)) +
                                         z11 * (xi - x.at(i)) * (yi - y.at(j))) /
                                        ((x.at(i + 1) - x.at(i)) * (y.at(j + 1) - y.at(j)));
                            zInterp.push_back(zi);
                            break;
                        }
                    }
                    break;
                }
            }
        }
        return zInterp;
    }
};

} // namespace example
} // namespace org