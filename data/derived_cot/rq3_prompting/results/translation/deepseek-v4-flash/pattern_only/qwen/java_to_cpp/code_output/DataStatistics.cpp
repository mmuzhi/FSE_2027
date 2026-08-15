#include <vector>
#include <algorithm>
#include <unordered_map>
#include <cmath>
#include <cstdint>
#include <limits>
#include <stdexcept>

class DataStatistics {
private:
    static double javaRound(double x) {
        if (std::isnan(x)) return 0.0;
        if (x >= static_cast<double>(std::numeric_limits<int64_t>::max())) {
            return static_cast<double>(std::numeric_limits<int64_t>::max());
        }
        if (x <= static_cast<double>(std::numeric_limits<int64_t>::min())) {
            return static_cast<double>(std::numeric_limits<int64_t>::min());
        }
        return std::floor(x + 0.5);
    }

    static double roundToTwo(double x) {
        return javaRound(x * 100.0) / 100.0;
    }

public:
    double mean(const std::vector<int>& data) const {
        uint32_t sum = 0;
        for (int x : data) {
            sum += static_cast<uint32_t>(x);
        }
        double sumDouble = static_cast<double>(static_cast<int32_t>(sum));
        return roundToTwo(sumDouble / static_cast<double>(data.size()));
    }

    double median(const std::vector<int>& data) const {
        if (data.empty()) {
            throw std::out_of_range("Index -1 out of bounds for length 0");
        }
        std::vector<int> sortedData = data;
        std::sort(sortedData.begin(), sortedData.end());
        size_t n = sortedData.size();

        if (n % 2 == 0) {
            size_t middle = n / 2;
            int a = sortedData[middle - 1];
            int b = sortedData[middle];
            uint32_t sum = static_cast<uint32_t>(a) + static_cast<uint32_t>(b);
            int32_t wrapped = static_cast<int32_t>(sum);
            return roundToTwo(static_cast<double>(wrapped) / 2.0);
        } else {
            return static_cast<double>(sortedData[n / 2]);
        }
    }

    std::vector<int> mode(const std::vector<int>& data) const {
        std::unordered_map<int, long long> freq;
        for (int x : data) {
            ++freq[x];
        }
        if (freq.empty()) {
            throw std::runtime_error("No value present");
        }

        long long maxCount = 0;
        for (const auto& entry : freq) {
            if (entry.second > maxCount) maxCount = entry.second;
        }

        std::vector<int> result;
        for (const auto& entry : freq) {
            if (entry.second == maxCount) result.push_back(entry.first);
        }
        std::sort(result.begin(), result.end());
        return result;
    }
};