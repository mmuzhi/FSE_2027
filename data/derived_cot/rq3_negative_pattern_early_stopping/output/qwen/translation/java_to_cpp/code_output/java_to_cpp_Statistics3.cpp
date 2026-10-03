#include <vector>
#include <algorithm>
#include <cmath>
#include <limits>
#include <optional>
#include <stdexcept>
#include <iostream>

class Statistics3 {
public:
    double median(const std::vector<int>& data) {
        std::vector<int> sortedData = data;
        std::sort(sortedData.begin(), sortedData.end());
        int n = sortedData.size();
        if (n % 2 == 1) {
            return sortedData[n / 2];
        } else {
            return (sortedData[n / 2 - 1] + sortedData[n / 2]) / 2.0;
        }
    }

    std::vector<int> mode(const std::vector<int>& data) {
        std::map<int, long> counts;
        for (int num : data) {
            counts[num]++;
        }
        long maxCount = 0;
        for (const auto& pair : counts) {
            if (pair.second > maxCount) {
                maxCount = pair.second;
            }
        }
        std::vector<int> modes;
        for (const auto& pair : counts) {
            if (pair.second == maxCount) {
                modes.push_back(pair.first);
            }
        }
        return modes;
    }

    std::optional<double> correlation(const std::vector<int>& x, const std::vector<int>& y) {
        if (x.empty() || x.size() != y.size()) {
            return std::nullopt;
        }
        double meanX = 0.0;
        double meanY = 0.0;
        for (int i = 0; i < x.size(); i++) {
            meanX += x[i];
            meanY += y[i];
        }
        meanX /= x.size();
        meanY /= y.size();

        double numerator = 0.0;
        double denomX = 0.0;
        double denomY = 0.0;

        for (int i = 0; i < x.size(); i++) {
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
        double average = 0.0;
        for (int num : data) {
            average += num;
        }
        average /= data.size();
        return average;
    }

    std::vector<std::vector<double>> correlationMatrix(const std::vector<std::vector<int>>& data) {
        int numCols = data[0].size();
        std::vector<std::vector<double>> matrix(numCols, std::vector<double>(numCols));

        for (int i = 0; i < numCols; i++) {
            std::vector<int> column1;
            for (const auto& row : data) {
                column1.push_back(row[i]);
            }
            for (int j = 0; j < numCols; j++) {
                std::vector<int> column2;
                for (const auto& row : data) {
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
            if (data.empty()) {
                throw std::runtime_error("Array is empty");
            }
            return std::nullopt;
        }
        auto m = mean(data);
        if (!m) {
            return std::nullopt;
        }
        double variance = 0.0;
        for (int num : data) {
            double diff = num - *m;
            variance += diff * diff;
        }
        variance /= (data.size() - 1);
        return std::sqrt(variance);
    }

    std::optional<std::vector<double>> zScore(const std::vector<int>& data) {
        auto m = mean(data);
        auto sd = standardDeviation(data);
        if (!m || !sd || *sd == 0) {
            return std::nullopt;
        }
        std::vector<double> result;
        for (int num : data) {
            double z = (num - *m) / *sd;
            result.push_back(z);
        }
        return result;
    }
};