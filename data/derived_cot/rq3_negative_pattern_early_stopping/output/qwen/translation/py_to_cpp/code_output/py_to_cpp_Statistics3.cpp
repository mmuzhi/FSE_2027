#include <vector>
#include <algorithm>
#include <cmath>
#include <iostream>
#include <map>

class Statistics3 {
public:
    static double median(std::vector<double> data) {
        std::sort(data.begin(), data.end());
        size_t n = data.size();
        if (n % 2 == 1) {
            return data[n / 2];
        } else {
            return (data[n / 2 - 1] + data[n / 2]) / 2.0;
        }
    }

    static std::vector<double> mode(std::vector<double> data) {
        std::map<double, int> counts;
        for (double value : data) {
            counts[value]++;
        }
        int max_count = 0;
        for (auto& pair : counts) {
            if (pair.second > max_count) {
                max_count = pair.second;
            }
        }
        std::vector<double> mode_values;
        for (auto& pair : counts) {
            if (pair.second == max_count) {
                mode_values.push_back(pair.first);
            }
        }
        return mode_values;
    }

    static double correlation(std::vector<double> x, std::vector<double> y) {
        size_t n = x.size();
        if (n != y.size() || n == 0) {
            return NAN;
        }
        double mean_x = 0.0, mean_y = 0.0;
        for (double xi : x) mean_x += xi;
        for (double yi : y) mean_y += yi;
        mean_x /= n;
        mean_y /= n;

        double numerator = 0.0;
        for (size_t i = 0; i < n; ++i) {
            numerator += (x[i] - mean_x) * (y[i] - mean_y);
        }

        double denominator = std::sqrt(
            std::accumulate(x.begin(), x.end(), 0.0, 
                [mean_x](double sum, double val) { return sum + (val - mean_x)*(val - mean_x); }) *
            std::accumulate(y.begin(), y.end(), 0.0, 
                [mean_y](double sum, double val) { return sum + (val - mean_y)*(val - mean_y); })
        );

        if (denominator == 0) {
            return NAN;
        }
        return numerator / denominator;
    }

    static double mean(std::vector<double> data) {
        if (data.empty()) {
            return NAN;
        }
        double sum = 0.0;
        for (double value : data) {
            sum += value;
        }
        return sum / data.size();
    }

    static std::vector<std::vector<double>> correlation_matrix(std::vector<std::vector<double>> data) {
        size_t rows = data.size();
        if (rows == 0) return {};
        size_t cols = data[0].size();

        std::vector<std::vector<double>> matrix;
        for (size_t i = 0; i < cols; ++i) {
            std::vector<double> row_i;
            for (size_t j = 0; j < cols; ++j) {
                std::vector<double> col1, col2;
                for (size_t k = 0; k < rows; ++k) {
                    col1.push_back(data[k][i]);
                    col2.push_back(data[k][j]);
                }
                double corr = correlation(col1, col2);
                row_i.push_back(corr);
            }
            matrix.push_back(row_i);
        }
        return matrix;
    }

    static double standard_deviation(std::vector<double> data) {
        size_t n = data.size();
        if (n < 2) {
            return NAN;
        }
        double mean_val = mean(data);
        double sum_sq = 0.0;
        for (double x : data) {
            sum_sq += (x - mean_val) * (x - mean_val);
        }
        return std::sqrt(sum_sq / (n - 1));
    }

    static std::vector<double> z_score(std::vector<double> data) {
        double mean_val = mean(data);
        double std_dev = standard_deviation(data);
        if (std_dev == 0 || std_dev == NAN) {
            return {};
        }
        std::vector<double> result;
        for (double x : data) {
            result.push_back((x - mean_val) / std_dev);
        }
        return result;
    }
};