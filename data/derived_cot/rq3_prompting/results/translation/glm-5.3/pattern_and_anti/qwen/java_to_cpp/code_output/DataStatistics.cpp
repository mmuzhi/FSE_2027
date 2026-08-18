#pragma once
#include <vector>
#include <map>
#include <algorithm>
#include <cmath>
#include <numeric>
#include <cstdint>

namespace org::example {

class DataStatistics {
public:
    double mean(const std::vector<int>& data) {
        // Java: int sum via IntStream, widened to double; rounding = floor(x + 0.5) (half-up)
        double sum = static_cast<double>(std::accumulate(data.begin(), data.end(), static_cast<int64_t>(0)));
        return javaRound((sum / static_cast<double>(data.size())) * 100.0) / 100.0;
    }

    double median(std::vector<int> data) {
        std::sort(data.begin(), data.end());
        std::size_t n = data.size();

        if (n % 2 == 0) {
            std::size_t middle = n / 2;
            return javaRound(((static_cast<double>(data[middle - 1]) + data[middle]) / 2.0) * 100.0) / 100.0;
        } else {
            std::size_t middle = n / 2;
            return static_cast<double>(data[middle]);
        }
    }

    std::vector<int> mode(const std::vector<int>& data) {
        std::map<int, long long> frequencyMap; // ordered map => keys already sorted
        for (int e : data) frequencyMap[e]++;

        long long maxCount = std::numeric_limits<long long>::min();
        for (const auto& [key, value] : frequencyMap)
            maxCount = std::max(maxCount, value); // mirrors Collections.max on values

        std::vector<int> result;
        for (const auto& [key, value] : frequencyMap)
            if (value == maxCount)
                result.push_back(key); // in-order iteration == .sorted()
        return result;
    }

private:
    // Java Math.round(double): floor(x + 0.5), with NaN -> 0
    static double javaRound(double x) {
        if (std::isnan(x)) return 0.0;
        return std::floor(x + 0.5);
    }
};

} // namespace org::example