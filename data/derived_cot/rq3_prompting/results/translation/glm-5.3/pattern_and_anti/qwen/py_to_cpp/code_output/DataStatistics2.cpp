#include <vector>
#include <cmath>
#include <numeric>
#include <algorithm>
#include <limits>
#include <stdexcept>
#include <cfloat>

class DataStatistics2 {
private:
    // Stored as a matrix (rows x cols). A 1D input becomes an n x 1 matrix,
    // so with rowvar=False semantics each column is one variable (matching np).
    std::vector<std::vector<double>> data;
    size_t rows;
    size_t cols;

    // Python's round(): round-half-to-even at the given decimal precision.
    static double py_round(double x, int digits) {
        double scale = std::pow(10.0, digits);
        return std::nearbyint(x * scale) / scale; // default FE_TONEAREST == half-to-even
    }

    std::vector<double> flatten() const {
        std::vector<double> v;
        v.reserve(rows * cols);
        for (const auto& r : data)
            v.insert(v.end(), r.begin(), r.end());
        return v;
    }

public:
    // 1D input: np.array([1, 2, 3, 4]) -> single variable, n observations
    DataStatistics2(const std::vector<double>& input) {
        rows = input.size();
        cols = 1;
        data.assign(rows, std::vector<double>(1));
        for (size_t i = 0; i < rows; ++i) data[i][0] = input[i];
    }

    // 2D input: np.array([[...], [...]]) kept row-major as-is
    DataStatistics2(const std::vector<std::vector<double>>& input)
        : data(input), rows(input.size()), cols(input.empty() ? 0 : input[0].size()) {}

    double get_sum() const {
        std::vector<double> v = flatten();
        if (v.empty()) throw std::runtime_error("sum of empty sequence"); // mirrors numpy ValueError
        return std::accumulate(v.begin(), v.end(), 0.0);
    }

    double get_min() const {
        std::vector<double> v = flatten();
        if (v.empty()) throw std::runtime_error("zero-size array to reduction operation minimum");
        return *std::min_element(v.begin(), v.end());
    }

    double get_max() const {
        std::vector<double> v = flatten();
        if (v.empty()) throw std::runtime_error("zero-size array to reduction operation maximum");
        return *std::max_element(v.begin(), v.end());
    }

    double get_variance() const {
        std::vector<double> v = flatten();
        if (v.empty()) throw std::runtime_error("variance of empty sequence");
        double n = static_cast<double>(v.size());
        double mean = std::accumulate(v.begin(), v.end(), 0.0) / n;
        double ss = 0.0;
        for (double x : v) ss += (x - mean) * (x - mean);
        return py_round(ss / n, 2); // ddof = 0, as np.var default
    }

    double get_std_deviation() const {
        std::vector<double> v = flatten();
        if (v.empty()) throw std::runtime_error("std of empty sequence");
        double n = static_cast<double>(v.size());
        double mean = std::accumulate(v.begin(), v.end(), 0.0) / n;
        double ss = 0.0;
        for (double x : v) ss += (x - mean) * (x - mean);
        return py_round(std::sqrt(ss / n), 2); // ddof = 0, as np.std default
    }

    // np.corrcoef(self.data, rowvar=False): k x k Pearson correlation
    // matrix over columns (variables); constant variable -> NaN (numpy semantics).
    std::vector<std::vector<double>> get_correlation() const {
        if (rows == 0 || cols == 0)
            throw std::runtime_error("corrcoef of empty array");

        std::vector<double> mean(cols, 0.0);
        for (const auto& r : data)
            for (size_t j = 0; j < cols; ++j) mean[j] += r[j];
        for (size_t j = 0; j < cols; ++j) mean[j] /= static_cast<double>(rows);

        std::vector<std::vector<double>> corr(cols, std::vector<double>(cols, 0.0));
        for (size_t i = 0; i < cols; ++i) {
            for (size_t j = 0; j < cols; ++j) {
                double cov = 0.0, vi = 0.0, vj = 0.0;
                for (size_t r = 0; r < rows; ++r) {
                    double di = data[r][i] - mean[i];
                    double dj = data[r][j] - mean[j];
                    cov += di * dj;
                    vi += di * di;
                    vj += dj * dj;
                }
                double denom = std::sqrt(vi) * std::sqrt(vj);
                corr[i][j] = (denom != 0.0)
                                 ? cov / denom
                                 : std::numeric_limits<double>::quiet_NaN();
            }
        }
        return corr;
    }
};