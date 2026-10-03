#include <vector>
#include <algorithm>
#include <unordered_map>
#include <cmath>
#include <optional>
#include <numeric>
#include <limits>
#include <stdexcept>

class Statistics3 {
public:
    double median(std::vector<int> data) {
        std::sort(data.begin(), data.end());
        size_t n = data.size();
        if (n % 2 == 1) {
            return data[n / 2];
        } else {
            return (data[n / 2 - 1] + data[n / 2]) / 2.0;
        }
    }

    std::vector<int> mode(const std::vector<int>& data) {
        std::unordered_map<int, long> counts;
        for (int e : data) {
            counts[e]++;
        }
        if (counts.empty()) {
            throw std::runtime_error("No elements in mode");
        }
        long maxCount = 0;
        for (const auto& [key, value] : counts) {
            maxCount = std::max(maxCount, value);
        }
        std::vector<int> result;
        for (const auto& [key, value] : counts) {
            if (value == maxCount) {
                result.push_back(key);
            }
        }
        return result;
    }

    std::optional<double> correlation(const std::vector<int>& x, const std::vector<int>& y) {
        if (x.size() != y.size() || x.empty()) {
            return std::nullopt;
        }

        double meanX = std::accumulate(x.begin(), x.end(), 0.0) / x.size();
        double meanY = std::accumulate(y.begin(), y.end(), 0.0) / y.size();

        double numerator = 0.0;
        double denomX = 0.0;
        double denomY = 0.0;

        for (size_t i = 0; i < x.size(); i++) {
            double diffX = x[i] - meanX;
            double diffY = y[i] - meanY;
            numerator += diffX * diffY;
            denomX += diffX * diffX;
            denomY += diffY * diffY;
        }

        if (denomX == 0 || denomY == 0) {
            return std::nullopt;
        }

        return numerator / std::sqrt(denomX * denomY);
    }

    std::optional<double> mean(const std::vector<int>& data) {
        if (data.empty()) {
            return std::nullopt;
        }
        return std::accumulate(data.begin(), data.end(), 0.0) / data.size();
    }

    std::vector<std::vector<double>> correlationMatrix(const std::vector<std::vector<int>>& data) {
        size_t numCols = data[0].size();
        std::vector<std::vector<double>> matrix(numCols, std::vector<double>(numCols));

        for (size_t i = 0; i < numCols; i++) {
            for (size_t j = 0; j < numCols; j++) {
                std::vector<int> column1;
                std::vector<int> column2;
                column1.reserve(data.size());
                column2.reserve(data.size());
                for (const auto& row : data) {
                    column1.push_back(row[i]);
                    column2.push_back(row[j]);
                }
                auto corr = correlation(column1, column2);
                matrix[i][j] = corr.has_value() ? corr.value() : std::numeric_limits<double>::quiet_NaN();
            }
        }

        return matrix;
    }

    std::optional<double> standardDeviation(const std::vector<int>& data) {
        if (data.size() < 2) {
            return std::nullopt;
        }
        double m = mean(data).value();
        double variance = 0.0;
        for (int x : data) {
            variance += std::pow(x - m, 2);
        }
        variance /= (data.size() - 1);
        return std::sqrt(variance);
    }

    std::optional<std::vector<double>> zScore(const std::vector<int>& data) {
        auto m = mean(data);
        auto stdDev = standardDeviation(data);
        if (!m.has_value() || !stdDev.has_value() || stdDev.value() == 0) {
            return std::nullopt;
        }
        std::vector<double> result;
        result.reserve(data.size());
        for (int x : data) {
            result.push_back((x - m.value()) / stdDev.value());
        }
        return result;
    }
};