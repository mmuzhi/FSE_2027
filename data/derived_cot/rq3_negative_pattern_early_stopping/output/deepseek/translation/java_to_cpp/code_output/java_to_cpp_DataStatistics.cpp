#include <vector>
#include <algorithm>
#include <cmath>
#include <unordered_map>
#include <cstdint>
#include <stdexcept>

class DataStatistics {
private:
    // Replicates Java's Math.round rounding half up (ties toward +inf)
    static double roundToTwoDecimals(double value) {
        return std::floor(value * 100.0 + 0.5) / 100.0;
    }

public:
    double mean(const std::vector<int>& data) {
        // Use long long to avoid overflow (Java uses int, but overflow is UB in C++)
        long long sum = 0;
        for (int v : data) {
            sum += v;
        }
        double result = static_cast<double>(sum) / data.size();
        return roundToTwoDecimals(result);
    }

    double median(const std::vector<int>& data) {
        std::vector<int> sortedData = data;
        std::sort(sortedData.begin(), sortedData.end());
        int n = sortedData.size();

        if (n % 2 == 0) {
            int middle = n / 2;
            double avg = (sortedData[middle - 1] + sortedData[middle]) / 2.0;
            return roundToTwoDecimals(avg);
        } else {
            int middle = n / 2;
            return static_cast<double>(sortedData[middle]);
        }
    }

    std::vector<int> mode(const std::vector<int>& data) {
        std::unordered_map<int, long long> freq;
        for (int v : data) {
            freq[v]++;
        }

        long long maxCount = 0;
        for (const auto& p : freq) {
            if (p.second > maxCount) {
                maxCount = p.second;
            }
        }

        std::vector<int> modes;
        for (const auto& p : freq) {
            if (p.second == maxCount) {
                modes.push_back(p.first);
            }
        }

        std::sort(modes.begin(), modes.end());
        return modes;
    }
};