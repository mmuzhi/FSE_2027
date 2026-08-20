#include <cstddef>
#include <vector>

namespace interpolation {

std::vector<double> interpolate1d(const std::vector<double>& x,
                                  const std::vector<double>& y,
                                  const std::vector<double>& xInterp) {
    std::vector<double> yInterp;
    for (double xi : xInterp) {
        // "i + 1 < x.size()" mirrors Java's "i < x.size() - 1" safely
        // (also skips the loop entirely when x is empty, like Java).
        for (std::size_t i = 0; i + 1 < x.size(); ++i) {
            if (x.at(i) <= xi && xi <= x.at(i + 1)) {
                double yi = y.at(i) +
                            (y.at(i + 1) - y.at(i)) * (xi - x.at(i)) /
                            (x.at(i + 1) - x.at(i));
                yInterp.push_back(yi);
                break;
            }
        }
    }
    return yInterp;
}

std::vector<double> interpolate2d(const std::vector<double>& x,
                                  const std::vector<double>& y,
                                  const std::vector<std::vector<double>>& z,
                                  const std::vector<double>& xInterp,
                                  const std::vector<double>& yInterp) {
    std::vector<double> zInterp;
    for (std::size_t k = 0; k < xInterp.size(); ++k) {
        double xi = xInterp.at(k);
        double yi = yInterp.at(k);
        for (std::size_t i = 0; i + 1 < x.size(); ++i) {
            if (x.at(i) <= xi && xi <= x.at(i + 1)) {
                for (std::size_t j = 0; j + 1 < y.size(); ++j) {
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
                // Note: this break is outside the j-loop, so if xi falls in an
                // x-interval but yi falls in no y-interval, nothing is appended
                // for this k (same as the Java version).
                break;
            }
        }
    }
    return zInterp;
}

}  // namespace interpolation