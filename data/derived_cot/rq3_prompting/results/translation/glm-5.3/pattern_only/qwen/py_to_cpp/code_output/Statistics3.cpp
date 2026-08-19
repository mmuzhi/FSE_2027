#include <algorithm>
#include <cmath>
#include <numeric>
#include <optional>
#include <stdexcept>
#include <utility>
#include <vector>

class Statistics3 {
public:
    // Returns the middle element (odd) or the average of the two middle
    // elements (even) of the sorted data. Empty input -> out_of_range
    // (mirrors Python IndexError).
    static double median(std::vector<double> data) {
        std::sort(data.begin(), data.end());
        std::size_t n = data.size();
        if (n % 2 == 1) {
            return data.at(n / 2);
        } else {
            return (data.at(n / 2 - 1) + data.at(n / 2)) / 2.0;
        }
    }

    // Returns all values tied for the highest count, in first-seen
    // (insertion) order, like a Python dict. Empty input -> invalid_argument
    // (mirrors max() on an empty sequence).
    static std::vector<double> mode(const std::vector<double>& data) {
        std::vector<std::pair<double, int>> counts;
        for (double value : data) {
            auto it = std::find_if(counts.begin(), counts.end(),
                                   [value](const std::pair<double, int>& p) {
                                       return p.first == value;
                                   });
            if (it != counts.end()) {
                it->second += 1;
            } else {
                counts.emplace_back(value, 1);
            }
        }
        if (counts.empty()) {
            throw std::invalid_argument("max(): arg is an empty sequence");
        }
        int max_count = counts.front().second;
        for (const auto& p : counts) {
            max_count = std::max(max_count, p.second);
        }
        std::vector<double> mode_values;
        for (const auto& p : counts) {
            if (p.second == max_count) {
                mode_values.push_back(p.first);
            }
        }
        return mode_values;
    }

    // Pearson correlation. nullopt when the denominator is 0 (Python None).
    // Numerator pairs only up to the shorter length (zip semantics); the
    // variance sums still run over the full lists, as in Python.
    static std::optional<double> correlation(const std::vector<double>& x,
                                             const std::vector<double>& y) {
        std::size_t n = x.size();
        if (n == 0 || y.empty()) {
            throw std::runtime_error("ZeroDivisionError: division by zero");
        }
        double mean_x = std::accumulate(x.begin(), x.end(), 0.0) / static_cast<double>(n);
        double mean_y = std::accumulate(y.begin(), y.end(), 0.0) / static_cast<double>(y.size());
        double numerator = 0.0;
        std::size_t m = std::min(x.size(), y.size());
        for (std::size_t k = 0; k < m; ++k) {
            numerator += (x[k] - mean_x) * (y[k] - mean_y);
        }
        double sum_x = 0.0;
        for (double xi : x) sum_x += (xi - mean_x) * (xi - mean_x);
        double sum_y = 0.0;
        for (double yi : y) sum_y += (yi - mean_y) * (yi - mean_y);
        double denominator = std::sqrt(sum_x * sum_y);
        if (denominator == 0.0) {
            return std::nullopt;
        }
        return numerator / denominator;
    }

    // Arithmetic mean; nullopt for empty input (Python None).
    static std::optional<double> mean(const std::vector<double>& data) {
        if (data.empty()) {
            return std::nullopt;
        }
        return std::accumulate(data.begin(), data.end(), 0.0) /
               static_cast<double>(data.size());
    }

    // Square correlation matrix of size len(data[0]) x len(data[0]).
    // Rows shorter than the first row -> out_of_range (mirrors IndexError).
    static std::vector<std::vector<std::optional<double>>>
    correlation_matrix(const std::vector<std::vector<double>>& data) {
        std::vector<std::vector<std::optional<double>>> matrix;
        std::size_t dim = data.at(0).size();
        matrix.reserve(dim);
        for (std::size_t i = 0; i < dim; ++i) {
            std::vector<std::optional<double>> row;
            row.reserve(dim);
            for (std::size_t j = 0; j < dim; ++j) {
                std::vector<double> column1;
                std::vector<double> column2;
                column1.reserve(data.size());
                column2.reserve(data.size());
                for (const auto& r : data) {
                    column1.push_back(r.at(i));
                    column2.push_back(r.at(j));
                }
                row.push_back(correlation(column1, column2));
            }
            matrix.push_back(std::move(row));
        }
        return matrix;
    }

    // Sample standard deviation (n - 1 denominator); nullopt if n < 2.
    static std::optional<double> standard_deviation(const std::vector<double>& data) {
        std::size_t n = data.size();
        if (n < 2) {
            return std::nullopt;
        }
        double mean_value = *mean(data);
        double variance = 0.0;
        for (double x : data) {
            variance += (x - mean_value) * (x - mean_value);
        }
        variance /= static_cast<double>(n - 1);
        return std::sqrt(variance);
    }

    // Standardized values; nullopt if the standard deviation is missing or 0.
    // (For n < 2 the Python version also returns None before using the mean.)
    static std::optional<std::vector<double>> z_score(const std::vector<double>& data) {
        std::optional<double> std_deviation = standard_deviation(data);
        if (!std_deviation.has_value() || *std_deviation == 0.0) {
            return std::nullopt;
        }
        double m = *mean(data);
        std::vector<double> result;
        result.reserve(data.size());
        for (double x : data) {
            result.push_back((x - m) / *std_deviation);
        }
        return result;
    }
};