#include <algorithm>
#include <cmath>
#include <limits>
#include <map>
#include <optional>
#include <stdexcept>
#include <vector>

namespace org::example {

class Statistics3 {
public:
    // Java: Arrays.copyOf + Arrays.sort; empty input throws (mirrored via .at()).
    double median(const std::vector<int>& data) {
        std::vector<int> sortedData(data);
        std::sort(sortedData.begin(), sortedData.end());
        int n = static_cast<int>(sortedData.size());
        if (n % 2 == 1) {
            return sortedData.at(n / 2);
        } else {
            return (sortedData.at(n / 2 - 1) + sortedData.at(n / 2)) / 2.0;
        }
    }

    // Java: groupingBy + counting + Collections.max (throws on empty -> mirrored).
    std::vector<int> mode(const std::vector<int>& data) {
        std::map<int, long long> counts;
        for (int e : data) {
            counts[e]++;
        }
        if (counts.empty()) {
            throw std::runtime_error("NoSuchElementException"); // Collections.max on empty
        }
        long long maxCount = std::max_element(
            counts.begin(), counts.end(),
            [](const auto& a, const auto& b) { return a.second < b.second; }
        )->second;
        std::vector<int> result;
        for (const auto& [key, value] : counts) {
            if (value == maxCount) {
                result.push_back(key);
            }
        }
        return result;
    }

    // Java returns Double (nullable) -> std::optional<double>.
    std::optional<double> correlation(const std::vector<int>& x, const std::vector<int>& y) {
        if (x.size() != y.size() || x.empty()) {
            return std::nullopt;
        }

        double meanX = averageOf(x);
        double meanY = averageOf(y);

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

    std::optional<double> mean(const std::vector<int>& data) {
        if (data.empty()) {
            return std::nullopt;
        }
        return averageOf(data);
    }

    // Java: data[0] on empty throws AIOOBE -> mirrored via .at().
    std::vector<std::vector<double>> correlationMatrix(const std::vector<std::vector<int>>& data) {
        int numCols = static_cast<int>(data.at(0).size());
        std::vector<std::vector<double>> matrix(numCols, std::vector<double>(numCols));

        for (int i = 0; i < numCols; i++) {
            for (int j = 0; j < numCols; j++) {
                std::vector<int> column1;
                std::vector<int> column2;
                column1.reserve(data.size());
                column2.reserve(data.size());
                for (const auto& row : data) {
                    column1.push_back(row.at(i)); // row[i] in Java throws if out of range
                    column2.push_back(row.at(j));
                }
                auto corr = correlation(column1, column2);
                matrix[i][j] = corr.has_value() ? *corr
                                                : std::numeric_limits<double>::quiet_NaN();
            }
        }

        return matrix;
    }

    std::optional<double> standardDeviation(const std::vector<int>& data) {
        if (data.size() < 2) {
            return std::nullopt;
        }
        double m = *mean(data);
        double variance = 0.0;
        for (int x : data) {
            variance += std::pow(x - m, 2.0);
        }
        variance /= static_cast<double>(data.size() - 1);
        return std::sqrt(variance);
    }

    // Java returns double[] or null -> std::optional<std::vector<double>>.
    std::optional<std::vector<double>> zScore(const std::vector<int>& data) {
        auto m = mean(data);
        auto stdDeviation = standardDeviation(data);
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

private:
    // Mirrors Java IntStream.average(): 64-bit integer sum, then converted to double.
    static double averageOf(const std::vector<int>& v) {
        long long sum = 0;
        for (int e : v) {
            sum += e;
        }
        return static_cast<double>(sum) / static_cast<double>(v.size());
    }
};

} // namespace org::example