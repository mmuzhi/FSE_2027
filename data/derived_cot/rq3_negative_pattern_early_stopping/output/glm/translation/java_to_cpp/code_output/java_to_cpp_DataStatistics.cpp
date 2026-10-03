#include <vector>
#include <numeric>
#include <cmath>
#include <algorithm>
#include <unordered_map>
#include <stdexcept>
#include <limits>

class DataStatistics {
private:
    static double roundJava(double x) {
        if (std::isnan(x)) return 0.0;
        if (x <= static_cast<double>(std::numeric_limits<long long>::min())) return static_cast<double>(std::numeric_limits<long long>::min());
        if (x >= static_cast<double>(std::numeric_limits<long long>::max())) return static_cast<double>(std::numeric_limits<long long>::max());
        return std::floor(x + 0.5);
    }

public:
    double mean(const std::vector<int>& data) {
        int sum = std::accumulate(data.begin(), data.end(), 0);
        return roundJava((static_cast<double>(sum) / data.size()) * 100.0) / 100.0;
    }

    double median(const std::vector<int>& data) {
        if (data.empty()) {
            throw std::out_of_range("Index -1 out of bounds for length 0");
        }
        std::vector<int> sortedData = data;
        std::sort(sortedData.begin(), sortedData.end());
        size_t n = sortedData.size();

        if (n % 2 == 0) {
            size_t middle = n / 2;
            return roundJava(((sortedData.at(middle - 1) + sortedData.at(middle)) / 2.0) * 100.0) / 100.0;
        } else {
            size_t middle = n / 2;
            return sortedData.at(middle);
        }
    }

    std::vector<int> mode(const std::vector<int>& data) {
        std::unordered_map<int, long> frequencyMap;
        for (int val : data) {
            frequencyMap[val]++;
        }
        if (frequencyMap.empty()) {
            throw std::runtime_error("No value present");
        }

        long maxCount = 0;
        for (const auto& pair : frequencyMap) {
            if (pair.second > maxCount) {
                maxCount = pair.second;
            }
        }

        std::vector<int> result;
        for (const auto& pair : frequencyMap) {
            if (pair.second == maxCount) {
                result.push_back(pair.first);
            }
        }

        std::sort(result.begin(), result.end());
        return result;
    }
};