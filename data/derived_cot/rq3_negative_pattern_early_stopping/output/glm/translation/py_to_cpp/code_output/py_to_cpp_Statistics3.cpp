#include <vector>
#include <algorithm>
#include <cmath>
#include <map>
#include <optional>
#include <numeric>

class Statistics3 {
public:
    static std::optional<double> median(std::vector<double> data) {
        std::sort(data.begin(), data.end());
        int n = static_cast<int>(data.size());
        if (n % 2 == 1) {
            return data[n / 2];
        } else {
            return (data[n / 2 - 1] + data[n / 2]) / 2.0;
        }
    }

    static std::vector<double> mode(const std::vector<double>& data) {
        std::map<double, int> counts;
        std::vector<double> order;
        for (double value : data) {
            if (counts.find(value) == counts.end()) {
                order.push_back(value);
            }
            counts[value]++;
        }
        int max_count = 0;
        for (const auto& kv : counts) {
            if (kv.second > max_count) {
                max_count = kv.second;
            }
        }
        std::vector<double> mode_values;
        for (double value : order) {
            if (counts[value] == max_count) {
                mode_values.push_back(value);
            }
        }
        return mode_values;
    }

    static std::optional<double> correlation(const std::vector<double>& x, const std::vector<double>& y) {
        int n = static_cast<int>(x.size());
        double mean_x = std::accumulate(x.begin(), x.end(), 0.0) / n;
        double mean_y = std::accumulate(y.begin(), y.end(), 0.0) / n;

        double numerator = 0.0;
        for (int i = 0; i < n; i++) {
            numerator += (x[i] - mean_x) * (y[i] - mean_y);
        }

        double sum_x = 0.0, sum_y = 0.0;
        for (int i = 0; i < n; i++) {
            sum_x += (x[i] - mean_x) * (x[i] - mean_x);
            sum_y += (y[i] - mean_y) * (y[i] - mean_y);
        }

        double denominator = std::sqrt(sum_x * sum_y);
        if (denominator == 0) {
            return std::nullopt;
        }
        return numerator / denominator;
    }

    static std::optional<double> mean(const std::vector<double>& data) {
        if (data.empty()) {
            return std::nullopt;
        }
        return std::accumulate(data.begin(), data.end(), 0.0) / data.size();
    }

    static std::vector<std::vector<std::optional<double>>> correlation_matrix(const std::vector<std::vector<double>>& data) {
        std::vector<std::vector<std::optional<double>>> matrix;
        int num_cols = static_cast<int>(data[0].size());
        for (int i = 0; i < num_cols; i++) {
            std::vector<std::optional<double>> row;
            for (int j = 0; j < num_cols; j++) {
                std::vector<double> column1, column2;
                for (int k = 0; k < static_cast<int>(data.size()); k++) {
                    column1.push_back(data[k][i]);
                    column2.push_back(data[k][j]);
                }
                row.push_back(correlation(column1, column2));
            }
            matrix.push_back(row);
        }
        return matrix;
    }

    static std::optional<double> standard_deviation(const std::vector<double>& data) {
        int n = static_cast<int>(data.size());
        if (n < 2) {
            return std::nullopt;
        }
        double mean_value = mean(data).value();
        double variance = 0.0;
        for (double x : data) {
            variance += (x - mean_value) * (x - mean_value);
        }
        variance /= (n - 1);
        return std::sqrt(variance);
    }

    static std::optional<std::vector<double>> z_score(const std::vector<double>& data) {
        auto mean_opt = mean(data);
        auto std_dev = standard_deviation(data);
        if (!std_dev.has_value() || std_dev.value() == 0) {
            return std::nullopt;
        }
        double mean_val = mean_opt.value();
        std::vector<double> result;
        for (double x : data) {
            result.push_back((x - mean_val) / std_dev.value());
        }
        return result;
    }
};