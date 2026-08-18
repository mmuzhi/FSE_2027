#include <algorithm>
#include <cmath>
#include <limits>
#include <numeric>
#include <optional>
#include <stdexcept>
#include <unordered_map>
#include <vector>

namespace org::example {

class Statistics3 {
public:
    double median(const std::vector<int>& data) const {
        std::vector<int> sortedData = data;
        std::sort(sortedData.begin(), sortedData.end());
        std::size_t n = sortedData.size();
        if (n % 2 == 1) {
            return static_cast<double>(sortedData[n / 2]);
        } else {
            return (sortedData[n / 2 - 1] + sortedData[n / 2]) / 2.0;
        }
    }

    std::vector<int> mode(const std::vector<int>& data) const {
        std::unordered_map<int, long long> counts;
        for (int e : data) {
            counts[e]++;
        }
        if (counts.empty()) {
            // Mirrors NoSuchElementException from Collections.max on empty values
            throw std::runtime_error("no elements");
        }
        long long maxCount = std::max_element(
                counts.begin(), counts.end(),
                [](const auto& a, const auto& b) { return a.second < b.second; })->second;
        std::vector<int> result;
        for (const auto& entry : counts) {
            if (entry.second == maxCount) {
                result.push_back(entry.first);
            }
        }
        return result;
    }

    std::optional<double> correlation(const std::vector<int>& x, const std::vector<int>& y) const {
        if (x.size() != y.size() || x.empty()) {
            return std::nullopt;
        }

        double meanX = std::accumulate(x.begin(), x.end(), 0.0) / x.size();
        double meanY = std::accumulate(y.begin(), y.end(), 0.0) / y.size();

        double numerator = 0.0;
        double denomX = 0.0;
        double denomY = 0.0;

        for (std::size_t i = 0; i < x.size(); i++) {
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

    std::optional<double> mean(const std::vector<int>& data) const {
        if (data.empty()) {
            return std::nullopt;
        }
        return std::accumulate(data.begin(), data.end(), 0.0) / data.size();
    }

    std::vector<std::vector<double>> correlationMatrix(const std::vector<std::vector<int>>& data) const {
        std::size_t numCols = data.at(0).size(); // at() mirrors ArrayIndexOutOfBoundsException on empty data
        std::vector<std::vector<double>> matrix(numCols, std::vector<double>(numCols));

        for (std::size_t i = 0; i < numCols; i++) {
            for (std::size_t j = 0; j < numCols; j++) {
                std::vector<int> column1;
                std::vector<int> column2;
                column1.reserve(data.size());
                column2.reserve(data.size());
                for (const auto& row : data) {
                    column1.push_back(row[i]);
                    column2.push_back(row[j]);
                }
                std::optional<double> c = correlation(column1, column2);
                matrix[i][j] = c.has_value() ? *c
                                             : std::numeric_limits<double>::quiet_NaN();
            }
        }

        return matrix;
    }

    std::optional<double> standardDeviation(const std::vector<int>& data) const {
        if (data.size() < 2) {
            return std::nullopt;
        }
        double m = *mean(data);
        double variance = 0.0;
        for (int x : data) {
            variance += std::pow(static_cast<double>(x) - m, 2);
        }
        variance /= static_cast<double>(data.size() - 1);
        return std::sqrt(variance);
    }

    std::optional<std::vector<double>> zScore(const std::vector<int>& data) const {
        std::optional<double> m = mean(data);
        std::optional<double> stdDeviation = standardDeviation(data);
        if (!m.has_value() || !stdDeviation.has_value() || *stdDeviation == 0) {
            return std::nullopt;
        }
        std::vector<double> result;
        result.reserve(data.size());
        for (int x : data) {
            result.push_back((x - *m) / *stdDeviation);
        }
        return result;
    }
};

} // namespace org::example