#include <vector>
#include <algorithm>
#include <cmath>
#include <unordered_map>
#include <numeric>
#include <optional>

class Statistics3 {
public:
    // Median: returns sorted middle value (average of two for even length)
    static double median(const std::vector<double>& data) {
        std::vector<double> sorted = data;
        std::sort(sorted.begin(), sorted.end());
        size_t n = sorted.size();
        if (n % 2 == 1) {
            return sorted[n / 2];
        } else {
            return (sorted[n / 2 - 1] + sorted[n / 2]) / 2.0;
        }
    }

    // Mode: returns list of most frequent values
    static std::vector<double> mode(const std::vector<double>& data) {
        std::unordered_map<double, int> counts;
        for (double v : data) {
            ++counts[v];
        }
        int max_count = 0;
        for (const auto& p : counts) {
            if (p.second > max_count) max_count = p.second;
        }
        std::vector<double> result;
        for (const auto& p : counts) {
            if (p.second == max_count) {
                result.push_back(p.first);
            }
        }
        return result;
    }

    // Correlation: Pearson correlation coefficient, returns nullopt if denominator is zero
    static std::optional<double> correlation(const std::vector<double>& x, const std::vector<double>& y) {
        size_t n = x.size();
        double mean_x = std::accumulate(x.begin(), x.end(), 0.0) / n;
        double mean_y = std::accumulate(y.begin(), y.end(), 0.0) / n;

        double numerator = 0.0;
        double var_x = 0.0;
        double var_y = 0.0;
        for (size_t i = 0; i < n; ++i) {
            double dx = x[i] - mean_x;
            double dy = y[i] - mean_y;
            numerator += dx * dy;
            var_x += dx * dx;
            var_y += dy * dy;
        }

        double denominator = std::sqrt(var_x * var_y);
        if (denominator == 0.0) {
            return std::nullopt;
        }
        return numerator / denominator;
    }

    // Mean: average, returns nullopt for empty list
    static std::optional<double> mean(const std::vector<double>& data) {
        if (data.empty()) {
            return std::nullopt;
        }
        return std::accumulate(data.begin(), data.end(), 0.0) / data.size();
    }

    // Correlation matrix: each entry is correlation between two columns
    static std::vector<std::vector<std::optional<double>>> correlation_matrix(const std::vector<std::vector<double>>& data) {
        size_t cols = data[0].size();
        std::vector<std::vector<std::optional<double>>> matrix(cols, std::vector<std::optional<double>>(cols));

        for (size_t i = 0; i < cols; ++i) {
            // Extract column i
            std::vector<double> col_i;
            col_i.reserve(data.size());
            for (const auto& row : data) {
                col_i.push_back(row[i]);
            }
            for (size_t j = 0; j < cols; ++j) {
                // Extract column j
                std::vector<double> col_j;
                col_j.reserve(data.size());
                for (const auto& row : data) {
                    col_j.push_back(row[j]);
                }
                matrix[i][j] = correlation(col_i, col_j);
            }
        }
        return matrix;
    }

    // Standard deviation (sample standard deviation, ddof=1)
    static std::optional<double> standard_deviation(const std::vector<double>& data) {
        size_t n = data.size();
        if (n < 2) {
            return std::nullopt;
        }
        auto mean_opt = mean(data);
        if (!mean_opt.has_value()) {
            return std::nullopt;
        }
        double mean_val = mean_opt.value();
        double variance = 0.0;
        for (double x : data) {
            variance += (x - mean_val) * (x - mean_val);
        }
        variance /= (n - 1);
        return std::sqrt(variance);
    }

    // Z-score: returns list of (x - mean)/std, or nullopt if std is zero or not computable
    static std::optional<std::vector<double>> z_score(const std::vector<double>& data) {
        auto mean_opt = mean(data);
        if (!mean_opt.has_value()) {
            return std::nullopt;
        }
        double mean_val = mean_opt.value();
        auto std_opt = standard_deviation(data);
        if (!std_opt.has_value() || std_opt.value() == 0.0) {
            return std::nullopt;
        }
        double std_val = std_opt.value();
        std::vector<double> result;
        result.reserve(data.size());
        for (double x : data) {
            result.push_back((x - mean_val) / std_val);
        }
        return result;
    }
};