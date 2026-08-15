#include <vector>
#include <optional>
#include <cmath>
#include <algorithm>
#include <unordered_map>
#include <stdexcept>
#include <limits>

class Statistics3 {
public:
    double median(const std::vector<int>& data) {
        if (data.empty()) {
            throw std::out_of_range("Array index out of range");
        }
        std::vector<int> sortedData = data;
        std::sort(sortedData.begin(), sortedData.end());
        std::size_t n = sortedData.size();
        if (n % 2 == 1) {
            return sortedData[n / 2];
        } else {
            return (sortedData[n / 2 - 1] + sortedData[n / 2]) / 2.0;
        }
    }

    std::vector<int> mode(const std::vector<int>& data) {
        std::unordered_map<int, long long> counts;
        for (int x : data) {
            counts[x]++;
        }
        if (counts.empty()) {
            throw std::runtime_error("No value present");
        }
        long long maxCount = 0;
        for (const auto& entry : counts) {
            if (entry.second > maxCount) {
                maxCount = entry.second;
            }
        }
        std::vector<int> result;
        for (const auto& entry : counts) {
            if (entry.second == maxCount) {
                result.push_back(entry.first);
            }
        }
        return result;
    }

    std::optional<double> correlation(const std::vector<int>& x, const std::vector<int>& y) {
        if (x.size() != y.size() || x.empty()) {
            return std::nullopt;
        }
        long long sumX = 0;
        long long sumY = 0;
        for (int v : x) sumX += v;
        for (int v : y) sumY += v;
        double meanX = static_cast<double>(sumX) / x.size();
        double meanY = static_cast<double>(sumY) / y.size();

        double numerator = 0.0;
        double denomX = 0.0;
        double denomY = 0.0;
        for (std::size_t i = 0; i < x.size(); ++i) {
            double diffX = x[i] - meanX;
            double diffY = y[i] - meanY;
            numerator += diffX * diffY;
            denomX += diffX * diffX;
            denomY += diffY * diffY;
        }
        if (denomX == 0.0 || denomY == 0.0) {
            return std::nullopt;
        }
        return numerator / std::sqrt(denomX * denomY);
    }

    std::optional<double> mean(const std::vector<int>& data) {
        if (data.empty()) {
            return std::nullopt;
        }
        long long sum = 0;
        for (int v : data) {
            sum += v;
        }
        return static_cast<double>(sum) / data.size();
    }

    std::vector<std::vector<double>> correlationMatrix(const std::vector<std::vector<int>>& data) {
        if (data.empty()) {
            throw std::out_of_range("Array index out of range");
        }
        std::size_t numCols = data[0].size();
        std::vector<std::vector<double>> matrix(numCols, std::vector<double>(numCols, 0.0));

        for (std::size_t i = 0; i < numCols; ++i) {
            for (std::size_t j = 0; j < numCols; ++j) {
                std::vector<int> column1(data.size());
                std::vector<int> column2(data.size());
                for (std::size_t r = 0; r < data.size(); ++r) {
                    column1[r] = data.at(r).at(i);
                    column2[r] = data.at(r).at(j);
                }
                auto corr = correlation(column1, column2);
                matrix[i][j] = corr.has_value() ? *corr : std::numeric_limits<double>::quiet_NaN();
            }
        }
        return matrix;
    }

    std::optional<double> standardDeviation(const std::vector<int>& data) {
        if (data.size() < 2) {
            return std::nullopt;
        }
        double meanValue = *mean(data);
        double variance = 0.0;
        for (int x : data) {
            variance += std::pow(x - meanValue, 2);
        }
        variance /= (data.size() - 1);
        return std::sqrt(variance);
    }

    std::optional<std::vector<double>> zScore(const std::vector<int>& data) {
        auto meanOpt = mean(data);
        auto stdOpt = standardDeviation(data);
        if (!meanOpt.has_value() || !stdOpt.has_value() || *stdOpt == 0.0) {
            return std::nullopt;
        }
        double meanValue = *meanOpt;
        double stdValue = *stdOpt;
        std::vector<double> result;
        result.reserve(data.size());
        for (int x : data) {
            result.push_back((x - meanValue) / stdValue);
        }
        return result;
    }
};