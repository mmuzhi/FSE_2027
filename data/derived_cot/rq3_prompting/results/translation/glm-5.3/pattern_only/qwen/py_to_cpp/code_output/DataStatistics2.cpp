#include <vector>
#include <cmath>
#include <numeric>
#include <algorithm>
#include <stdexcept>

class DataStatistics2 {
private:
    std::vector<std::vector<double>> data_;  // rows of the (possibly 1-D) dataset
    bool is1D_;                              // tracks np.array(list) vs np.array(nested list)

    // Python round(x, 2) / np.round: round-half-to-even on 2 decimals
    static double round2(double x) {
        return std::nearbyint(x * 100.0) / 100.0;
    }

    std::vector<double> flatten() const {
        std::vector<double> out;
        for (const auto& row : data_)
            out.insert(out.end(), row.begin(), row.end());
        return out;
    }

    double variance_raw() const {
        std::vector<double> flat = flatten();
        size_t n = flat.size();
        if (n == 0) return std::nan("");  // np.var([]) -> nan (with warning)
        double mean = std::accumulate(flat.begin(), flat.end(), 0.0) /
                      static_cast<double>(n);
        double acc = 0.0;
        for (double v : flat) {
            double d = v - mean;
            acc += d * d;
        }
        return acc / static_cast<double>(n);  // ddof=0 (population variance)
    }

public:
    // 1-D input: np.array(data)
    DataStatistics2(const std::vector<double>& data)
        : data_{std::vector<std::vector<double>>{data}}, is1D_(true) {}

    // 2-D input: np.array(nested data)
    DataStatistics2(const std::vector<std::vector<double>>& data)
        : data_(data), is1D_(false) {}

    double get_sum() const {
        double s = 0.0;  // np.sum([]) == 0.0
        for (const auto& row : data_)
            for (double v : row) s += v;
        return s;
    }

    double get_min() const {
        double m = 0.0;
        bool first = true;
        for (const auto& row : data_)
            for (double v : row) {
                if (first) { m = v; first = false; }
                else m = std::min(m, v);
            }
        if (first)
            throw std::runtime_error(
                "zero-size array to reduction operation which has no identity");
        return m;
    }

    double get_max() const {
        double m = 0.0;
        bool first = true;
        for (const auto& row : data_)
            for (double v : row) {
                if (first) { m = v; first = false; }
                else m = std::max(m, v);
            }
        if (first)
            throw std::runtime_error(
                "zero-size array to reduction operation which has no identity");
        return m;
    }

    double get_variance() const {
        return round2(variance_raw());
    }

    double get_std_deviation() const {
        return round2(std::sqrt(variance_raw()));
    }

    // np.corrcoef(data, rowvar=False): columns are variables, rows are
    // observations; returns an n_vars x n_vars matrix.
    // A 1-D input is a single variable -> 1x1 matrix [[1.0]].
    std::vector<std::vector<double>> get_correlation() const {
        size_t nobs = data_.size();
        size_t nvars = is1D_ ? (nobs ? 1 : 0)
                             : (nobs ? data_[0].size() : 0);

        // Extract each variable (column) as a vector of observations
        std::vector<std::vector<double>> vars(nvars, std::vector<double>(nobs));
        if (is1D_) {
            for (size_t i = 0; i < nobs; ++i) vars[0][i] = data_[i][0];
        } else {
            for (size_t j = 0; j < nvars; ++j)
                for (size_t i = 0; i < nobs; ++i)
                    vars[j][i] = data_[i][j];
        }

        std::vector<std::vector<double>> corr(nvars,
                                              std::vector<double>(nvars, 0.0));
        for (size_t a = 0; a < nvars; ++a) {
            for (size_t b = a; b < nvars; ++b) {
                if (nobs == 0) {
                    corr[a][b] = corr[b][a] = std::nan("");
                    continue;
                }
                double ma = 0.0, mb = 0.0;
                for (size_t i = 0; i < nobs; ++i) {
                    ma += vars[a][i];
                    mb += vars[b][i];
                }
                ma /= static_cast<double>(nobs);
                mb /= static_cast<double>(nobs);
                double cov = 0.0, va = 0.0, vb = 0.0;
                for (size_t i = 0; i < nobs; ++i) {
                    double da = vars[a][i] - ma;
                    double db = vars[b][i] - mb;
                    cov += da * db;
                    va += da * da;
                    vb += db * db;
                }
                double denom = std::sqrt(va) * std::sqrt(vb);
                // ddof cancels out in Pearson correlation
                double r = (denom == 0.0) ? std::nan("") : (cov / denom);
                corr[a][b] = corr[b][a] = r;
            }
        }
        return corr;
    }
};