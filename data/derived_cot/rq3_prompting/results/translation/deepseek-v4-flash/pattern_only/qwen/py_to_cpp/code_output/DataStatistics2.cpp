#include <vector>
#include <cmath>
#include <stdexcept>
#include <limits>

class DataStatistics2 {
public:
    DataStatistics2(const std::vector<double>& data) {
        mat.resize(data.size());
        for (size_t i = 0; i < data.size(); ++i) {
            mat[i].resize(1);
            mat[i][0] = data[i];
        }
    }

    DataStatistics2(const std::vector<std::vector<double>>& data) {
        if (!data.empty()) {
            size_t cols = data[0].size();
            for (const auto& row : data) {
                if (row.size() != cols) {
                    throw std::invalid_argument("inhomogeneous shape");
                }
            }
        }
        mat = data;
    }

    double get_sum() const {
        double sum = 0.0;
        for (const auto& row : mat) {
            for (double x : row) {
                sum += x;
            }
        }
        return sum;
    }

    double get_min() const {
        if (total_count() == 0) {
            throw std::invalid_argument("zero-size array to reduction operation minimum which has no identity");
        }
        double min_val = mat[0][0];
        if (std::isnan(min_val)) return min_val;
        for (const auto& row : mat) {
            for (double x : row) {
                if (std::isnan(x)) return x;
                if (x < min_val) min_val = x;
            }
        }
        return min_val;
    }

    double get_max() const {
        if (total_count() == 0) {
            throw std::invalid_argument("zero-size array to reduction operation maximum which has no identity");
        }
        double max_val = mat[0][0];
        if (std::isnan(max_val)) return max_val;
        for (const auto& row : mat) {
            for (double x : row) {
                if (std::isnan(x)) return x;
                if (x > max_val) max_val = x;
            }
        }
        return max_val;
    }

    double get_variance() const {
        return round_to_2(variance_unrounded());
    }

    double get_std_deviation() const {
        return round_to_2(std::sqrt(variance_unrounded()));
    }

    std::vector<std::vector<double>> get_correlation() const {
        if (mat.empty()) {
            return {{std::numeric_limits<double>::quiet_NaN()}};
        }
        size_t rows = mat.size();
        size_t cols = mat[0].size();
        if (cols == 0) {
            return {};
        }

        std::vector<double> mean(cols, 0.0);
        for (size_t j = 0; j < cols; ++j) {
            double sum = 0.0;
            for (size_t i = 0; i < rows; ++i) {
                sum += mat[i][j];
            }
            mean[j] = sum / static_cast<double>(rows);
        }

        std::vector<double> sum_sq(cols, 0.0);
        for (size_t j = 0; j < cols; ++j) {
            double s = 0.0;
            for (size_t i = 0; i < rows; ++i) {
                double diff = mat[i][j] - mean[j];
                s += diff * diff;
            }
            sum_sq[j] = s;
        }

        std::vector<std::vector<double>> corr(cols, std::vector<double>(cols, 0.0));
        for (size_t i = 0; i < cols; ++i) {
            for (size_t j = 0; j < cols; ++j) {
                if (sum_sq[i] == 0.0 || sum_sq[j] == 0.0) {
                    corr[i][j] = std::numeric_limits<double>::quiet_NaN();
                } else if (i == j) {
                    corr[i][j] = 1.0;
                } else {
                    double cov = 0.0;
                    for (size_t k = 0; k < rows; ++k) {
                        cov += (mat[k][i] - mean[i]) * (mat[k][j] - mean[j]);
                    }
                    corr[i][j] = cov / std::sqrt(sum_sq[i] * sum_sq[j]);
                }
            }
        }
        return corr;
    }

private:
    std::vector<std::vector<double>> mat;

    size_t total_count() const {
        size_t n = 0;
        for (const auto& row : mat) {
            n += row.size();
        }
        return n;
    }

    double variance_unrounded() const {
        size_t n = total_count();
        if (n == 0) {
            return std::numeric_limits<double>::quiet_NaN();
        }
        double sum = 0.0;
        for (const auto& row : mat) {
            for (double x : row) {
                sum += x;
            }
        }
        double mean = sum / static_cast<double>(n);
        double var = 0.0;
        for (const auto& row : mat) {
            for (double x : row) {
                double diff = x - mean;
                var += diff * diff;
            }
        }
        return var / static_cast<double>(n);
    }

    static double round_to_2(double x) {
        if (std::isnan(x) || std::isinf(x)) return x;
        double scale = 100.0;
        double y = x * scale;
        double lower = std::floor(y);
        double upper = std::ceil(y);
        double diff_lower = y - lower;
        double diff_upper = upper - y;
        double result;
        if (diff_lower < diff_upper) {
            result = lower;
        } else if (diff_upper < diff_lower) {
            result = upper;
        } else {
            if (std::fmod(lower, 2.0) == 0.0) {
                result = lower;
            } else {
                result = upper;
            }
        }
        return result / scale;
    }
};