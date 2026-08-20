/**
 * A class implementing methods for calculating statistical indicators such as
 * median, mode, correlation matrix, and Z-score.
 *
 * Python's `None` results are represented with std::optional.
 * Python exceptions are mirrored with C++ exceptions:
 *   - IndexError       -> std::out_of_range
 *   - ValueError       -> std::invalid_argument
 *   - ZeroDivisionError-> std::invalid_argument
 */

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <numeric>
#include <optional>
#include <stdexcept>
#include <vector>

class Statistics3 {
public:
    // Calculates the median of the given list.
    static double median(std::vector<double> data) {
        std::sort(data.begin(), data.end());  // sorted(data) -> new sorted list
        std::size_t n = data.size();
        if (n % 2 == 1) {
            return data[n / 2];
        }
        if (n == 0) {
            // Python: sorted_data[n // 2 - 1] == sorted_data[-1] -> IndexError
            throw std::out_of_range("list index out of range");
        }
        return (data[n / 2 - 1] + data[n / 2]) / 2.0;
    }

    // Calculates the mode(s) of the given list: all values having the highest
    // count, in order of first appearance (Python dicts preserve insertion order).
    static std::vector<double> mode(const std::vector<double>& data) {
        std::vector<double> values;      // distinct values, insertion order
        std::vector<std::size_t> counts;

        for (const double& value : data) {
            auto it = std::find(values.begin(), values.end(), value);
            if (it == values.end()) {
                values.push_back(value);
                counts.push_back(1);
            } else {
                ++counts[static_cast<std::size_t>(it - values.begin())];
            }
        }

        if (values.empty()) {
            // Python: max() on an empty sequence -> ValueError
            throw std::invalid_argument("max() arg is an empty sequence");
        }

        std::size_t max_count = *std::max_element(counts.begin(), counts.end());
        std::vector<double> mode_values;
        for (std::size_t k = 0; k < values.size(); ++k) {
            if (counts[k] == max_count) {
                mode_values.push_back(values[k]);
            }
        }
        return mode_values;
    }

    // Calculates the Pearson correlation of the given lists.
    // Returns std::nullopt when the denominator is zero (Python's None).
    static std::optional<double> correlation(const std::vector<double>& x, const std::vector<double>& y) {
        std::size_t n = x.size();
        if (n == 0) {
            // Python: sum(x) / n with n == 0 -> ZeroDivisionError
            throw std::invalid_argument("division by zero");
        }
        double mean_x = std::accumulate(x.begin(), x.end(), 0.0) / static_cast<double>(n);
        double mean_y = std::accumulate(y.begin(), y.end(), 0.0) / static_cast<double>(n);

        // sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)):
        // zip() truncates to the shorter sequence.
        double numerator = 0.0;
        std::size_t zipped = std::min(x.size(), y.size());
        for (std::size_t i = 0; i < zipped; ++i) {
            numerator += (x[i] - mean_x) * (y[i] - mean_y);
        }

        double sum_sq_x = 0.0;
        for (const double& xi : x) {
            sum_sq_x += (xi - mean_x) * (xi - mean_x);
        }
        double sum_sq_y = 0.0;
        for (const double& yi : y) {
            sum_sq_y += (yi - mean_y) * (yi - mean_y);
        }

        double denominator = std::sqrt(sum_sq_x * sum_sq_y);
        if (denominator == 0.0) {
            return std::nullopt;
        }
        return numerator / denominator;
    }

    // Calculates the mean of the given list; std::nullopt for empty input (Python's None).
    static std::optional<double> mean(const std::vector<double>& data) {
        if (data.empty()) {
            return std::nullopt;
        }
        return std::accumulate(data.begin(), data.end(), 0.0) / static_cast<double>(data.size());
    }

    // Calculates the correlation matrix of the columns of the given data.
    static std::vector<std::vector<std::optional<double>>> correlation_matrix(const std::vector<std::vector<double>>& data) {
        if (data.empty()) {
            // Python: data[0] -> IndexError
            throw std::out_of_range("list index out of range");
        }
        std::vector<std::vector<std::optional<double>>> matrix;
        const std::size_t num_cols = data[0].size();
        matrix.reserve(num_cols);
        for (std::size_t i = 0; i < num_cols; ++i) {
            std::vector<std::optional<double>> row;
            row.reserve(num_cols);
            for (std::size_t j = 0; j < num_cols; ++j) {
                // Python builds the columns with list comprehensions whose `row`
                // loop variable lives in the comprehension scope only; `r` is used
                // here so the outer `row` is not shadowed (row.append must hit it).
                std::vector<double> column1;
                std::vector<double> column2;
                column1.reserve(data.size());
                column2.reserve(data.size());
                for (const std::vector<double>& r : data) {
                    column1.push_back(r.at(i));  // .at() mirrors IndexError on short rows
                    column2.push_back(r.at(j));
                }
                row.push_back(correlation(column1, column2));
            }
            matrix.push_back(std::move(row));
        }
        return matrix;
    }

    // Calculates the sample standard deviation (divisor n - 1);
    // std::nullopt when the list has fewer than 2 elements (Python's None).
    static std::optional<double> standard_deviation(const std::vector<double>& data) {
        std::size_t n = data.size();
        if (n < 2) {
            return std::nullopt;
        }
        double mean_value = *mean(data);
        double variance = 0.0;
        for (const double& x : data) {
            variance += (x - mean_value) * (x - mean_value);
        }
        variance /= static_cast<double>(n - 1);
        return std::sqrt(variance);
    }

    // Calculates the z-scores of the given list; std::nullopt when the
    // standard deviation is None or zero (Python's None).
    static std::optional<std::vector<double>> z_score(const std::vector<double>& data) {
        std::optional<double> mean_value = mean(data);
        std::optional<double> std_deviation = standard_deviation(data);
        if (!std_deviation.has_value() || *std_deviation == 0.0) {
            return std::nullopt;
        }
        std::vector<double> result;
        result.reserve(data.size());
        for (const double& x : data) {
            result.push_back((x - *mean_value) / *std_deviation);
        }
        return result;
    }
};