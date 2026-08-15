#include <vector>
#include <optional>
#include <algorithm>
#include <numeric>
#include <cmath>
#include <stdexcept>

class Statistics3 {
public:
    static double median(const std::vector<double>& data) {
        if (data.empty()) {
            throw std::out_of_range("index out of range");
        }
        std::vector<double> sorted_data = data;
        std::sort(sorted_data.begin(), sorted_data.end());
        size_t n = sorted_data.size();
        if (n % 2 == 1) {
            return sorted_data[n / 2];
        } else {
            return (sorted_data[n / 2 - 1] + sorted_data[n / 2]) / 2.0;
        }
    }

    static std::vector<double> mode(const std::vector<double>& data) {
        if (data.empty()) {
            throw std::invalid_argument("max() arg is an empty sequence");
        }
        std::vector<double> unique_values;
        std::vector<int> counts;
        for (double value : data) {
            bool found = false;
            for (size_t i = 0; i < unique_values.size(); ++i) {
                if (unique_values[i] == value) {
                    counts[i]++;
                    found = true;
                    break;
                }
            }
            if (!found) {
                unique_values.push_back(value);
                counts.push_back(1);
            }
        }
        int max_count = *std::max_element(counts.begin(), counts.end());
        std::vector<double> mode_values;
        for (size_t i = 0; i < unique_values.size(); ++i) {
            if (counts[i] == max_count) {
                mode_values.push_back(unique_values[i]);
            }
        }
        return mode_values;
    }

    static std::optional<double> correlation(const std::vector<double>& x, const std::vector<double>& y) {
        size_t n = x.size();
        if (n == 0) {
            throw std::invalid_argument("division by zero");
        }
        double mean_x = std::accumulate(x.begin(), x.end(), 0.0) / static_cast<double>(n);
        double mean_y = std::accumulate(y.begin(), y.end(), 0.0) / static_cast<double>(n);

        double numerator = 0.0;
        size_t m = std::min(x.size(), y.size());
        for (size_t i = 0; i < m; ++i) {
            numerator += (x[i] - mean_x) * (y[i] - mean_y);
        }

        double sum_x = 0.0;
        for (double xi : x) {
            sum_x += (xi - mean_x) * (xi - mean_x);
        }
        double sum_y = 0.0;
        for (double yi : y) {
            sum_y += (yi - mean_y) * (yi - mean_y);
        }

        double denominator = std::sqrt(sum_x * sum_y);
        if (denominator == 0.0) {
            return std::nullopt;
        }
        return numerator / denominator;
    }

    static std::optional<double> mean(const std::vector<double>& data) {
        if (data.empty()) {
            return std::nullopt;
        }
        return std::accumulate(data.begin(), data.end(), 0.0) / static_cast<double>(data.size());
    }

    static std::vector<std::vector<std::optional<double>>> correlation_matrix(
        const std::vector<std::vector<double>>& data) {
        if (data.empty() || data[0].empty()) {
            throw std::out_of_range("index out of range");
        }
        size_t cols = data[0].size();
        std::vector<std::vector<std::optional<double>>> matrix(
            cols, std::vector<std::optional<double>>(cols));

        for (size_t i = 0; i < cols; ++i) {
            for (size_t j = 0; j < cols; ++j) {
                std::vector<double> column1;
                std::vector<double> column2;
                for (const auto& row : data) {
                    column1.push_back(row.at(i));
                    column2.push_back(row.at(j));
                }
                matrix[i][j] = correlation(column1, column2);
            }
        }
        return matrix;
    }

    static std::optional<double> standard_deviation(const std::vector<double>& data) {
        size_t n = data.size();
        if (n < 2) {
            return std::nullopt;
        }
        auto mean_value = mean(data);
        double mean_val = *mean_value;
        double variance = 0.0;
        for (double x : data) {
            variance += (x - mean_val) * (x - mean_val);
        }
        variance /= static_cast<double>(n - 1);
        return std::sqrt(variance);
    }

    static std::optional<std::vector<double>> z_score(const std::vector<double>& data) {
        auto mean_value = mean(data);
        auto std_deviation = standard_deviation(data);
        if (!std_deviation.has_value() || *std_deviation == 0.0) {
            return std::nullopt;
        }
        std::vector<double> result;
        result.reserve(data.size());
        double mean_val = *mean_value;
        for (double x : data) {
            result.push_back((x - mean_val) / *std_deviation);
        }
        return result;
    }
};