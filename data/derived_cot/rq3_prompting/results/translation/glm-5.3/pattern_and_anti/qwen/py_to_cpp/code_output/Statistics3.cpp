#include <algorithm>
#include <cmath>
#include <optional>
#include <stdexcept>
#include <unordered_map>
#include <unordered_set>
#include <vector>

class Statistics3 {
public:
    // Python raises IndexError for empty input; mirror with out_of_range.
    static double median(std::vector<double> data) {
        std::sort(data.begin(), data.end());
        const size_t n = data.size();
        if (n % 2 == 1) {
            return data.at(n / 2);
        }
        if (n == 0) throw std::out_of_range("median(): empty sequence");
        return (data.at(n / 2 - 1) + data.at(n / 2)) / 2.0;
    }

    // Python: max() on empty counts raises ValueError; mirror it.
    // Result order follows first occurrence (Python dict insertion order).
    static std::vector<double> mode(const std::vector<double>& data) {
        std::unordered_map<double, int> counts;
        for (double value : data) {
            counts[value] = counts[value] + 1;
        }
        if (counts.empty()) throw std::invalid_argument("max(): empty sequence");
        int max_count = 0;
        for (const auto& kv : counts) max_count = std::max(max_count, kv.second);
        std::vector<double> mode_values;
        std::unordered_set<double> seen;
        for (double value : data) {
            if (counts[value] == max_count && seen.insert(value).second) {
                mode_values.push_back(value);
            }
        }
        return mode_values;
    }

    // Faithful to Python quirks: n = len(x) is used for BOTH means;
    // zip truncates numerator to the shorter list; denominator uses full lists.
    // Returns nullopt instead of None; throws on empty x (ZeroDivisionError analog).
    static std::optional<double> correlation(const std::vector<double>& x,
                                             const std::vector<double>& y) {
        const size_t n = x.size();
        if (n == 0) throw std::runtime_error("ZeroDivisionError: division by zero");
        double sum_x = 0.0, sum_y = 0.0;
        for (double v : x) sum_x += v;
        for (double v : y) sum_y += v;
        const double mean_x = sum_x / static_cast<double>(n);
        const double mean_y = sum_y / static_cast<double>(n);
        double numerator = 0.0;
        const size_t m = std::min(x.size(), y.size());
        for (size_t k = 0; k < m; ++k) {
            numerator += (x[k] - mean_x) * (y[k] - mean_y);
        }
        double sq_x = 0.0, sq_y = 0.0;
        for (double v : x) sq_x += (v - mean_x) * (v - mean_x);
        for (double v : y) sq_y += (v - mean_y) * (v - mean_y);
        const double denominator = std::sqrt(sq_x * sq_y);
        if (denominator == 0.0) return std::nullopt;
        return numerator / denominator;
    }

    static std::optional<double> mean(const std::vector<double>& data) {
        if (data.empty()) return std::nullopt;
        double s = 0.0;
        for (double v : data) s += v;
        return s / static_cast<double>(data.size());
    }

    // Python uses len(data[0]) for both loops; .at() mirrors IndexError on short rows.
    static std::vector<std::vector<std::optional<double>>>
    correlation_matrix(const std::vector<std::vector<double>>& data) {
        std::vector<std::vector<std::optional<double>>> matrix;
        const size_t cols = data.at(0).size();
        for (size_t i = 0; i < cols; ++i) {
            std::vector<std::optional<double>> row;
            for (size_t j = 0; j < cols; ++j) {
                std::vector<double> column1, column2;
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

    static std::optional<double> standard_deviation(const std::vector<double>& data) {
        const size_t n = data.size();
        if (n < 2) return std::nullopt;
        const double mean_value = *mean(data);
        double variance = 0.0;
        for (double v : data) variance += (v - mean_value) * (v - mean_value);
        variance /= static_cast<double>(n - 1);
        return std::sqrt(variance);
    }

    static std::optional<std::vector<double>> z_score(const std::vector<double>& data) {
        const std::optional<double> m = mean(data);
        const std::optional<double> std_deviation = standard_deviation(data);
        if (!std_deviation || *std_deviation == 0.0) return std::nullopt;
        std::vector<double> result;
        result.reserve(data.size());
        for (double v : data) result.push_back((v - *m) / *std_deviation);
        return result;
    }
};