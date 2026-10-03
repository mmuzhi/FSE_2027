#include <vector>
#include <algorithm>
#include <map>
#include <cmath>
#include <optional>
#include <numeric>
#include <iterator>

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
        std::map<int, long> counts;
        for (int x : data) {
            counts[x]++;
        }
        long maxCount = 0;
        for (const auto& p : counts) {
            if (p.second > maxCount) maxCount = p.second;
        }
        std::vector<int> result;
        for (const auto& p : counts) {
            if (p.second == maxCount) {
                result.push_back(p.first);
            }
        }
        return result;
    }

    std::optional<double> correlation(const std::vector<int>& x, const std::vector<int>& y) {
        if (x.size() != y.size() || x.empty()) {
            return std::nullopt;
        }
        double meanX = 0.0, meanY = 0.0;
        for (int v : x) meanX += v;
        for (int v : y) meanY += v;
        meanX /= x.size();
        meanY /= y.size();

        double numerator = 0.0, denomX = 0.0, denomY = 0.0;
        for (size_t i = 0; i < x.size(); ++i) {
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
        double sum = std::accumulate(data.begin(), data.end(), 0.0);
        return sum / data.size();
    }

    std::vector<std::vector<double>> correlationMatrix(const std::vector<std::vector<int>>& data) {
        if (data.empty() || data[0].empty()) return {};
        size_t numCols = data[0].size();
        std::vector<std::vector<double>> matrix(numCols, std::vector<double>(numCols, 0.0));
        for (size_t i = 0; i < numCols; ++i) {
            for (size_t j = 0; j < numCols; ++j) {
                std::vector<int> col1, col2;
                for (const auto& row : data) {
                    col1.push_back(row[i]);
                    col2.push_back(row[j]);
                }
                auto c = correlation(col1, col2);
                matrix[i][j] = c.has_value() ? c.value() : std::numeric_limits<double>::quiet_NaN();
            }
        }
        return matrix;
    }

    std::optional<double> standardDeviation(const std::vector<int>& data) {
        if (data.size() < 2) {
            return std::nullopt;
        }
        auto m = mean(data);
        if (!m.has_value()) return std::nullopt;
        double meanVal = m.value();
        double variance = 0.0;
        for (int x : data) {
            variance += (x - meanVal) * (x - meanVal);
        }
        variance /= (data.size() - 1);
        return std::sqrt(variance);
    }

    std::optional<std::vector<double>> zScore(const std::vector<int>& data) {
        auto m = mean(data);
        auto sd = standardDeviation(data);
        if (!m.has_value() || !sd.has_value() || sd.value() == 0.0) {
            return std::nullopt;
        }
        double meanVal = m.value();
        double sdVal = sd.value();
        std::vector<double> result;
        result.reserve(data.size());
        for (int x : data) {
            result.push_back((x - meanVal) / sdVal);
        }
        return result;
    }
};