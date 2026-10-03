#include <vector>
#include <algorithm>
#include <map>
#include <numeric>
#include <stdexcept>
#include <cmath>

class DataStatistics {
public:
    double mean(const std::vector<double>& data) {
        if (data.empty()) {
            throw std::invalid_argument("Data is empty");
        }
        double sum = std::accumulate(data.begin(), data.end(), 0.0);
        double result = sum / static_cast<double>(data.size());
        // round to two decimal places
        return std::round(result * 100.0) / 100.0;
    }

    double median(const std::vector<double>& data) {
        if (data.empty()) {
            throw std::invalid_argument("Data is empty");
        }
        std::vector<double> sorted = data;
        std::sort(sorted.begin(), sorted.end());
        size_t n = sorted.size();
        double result;
        if (n % 2 == 0) {
            size_t middle = n / 2;
            result = (sorted[middle - 1] + sorted[middle]) / 2.0;
        } else {
            size_t middle = n / 2;
            result = sorted[middle];
        }
        return std::round(result * 100.0) / 100.0;
    }

    std::vector<double> mode(const std::vector<double>& data) {
        if (data.empty()) {
            throw std::invalid_argument("Data is empty");
        }
        std::map<double, int> counter;
        for (double val : data) {
            counter[val]++;
        }
        int max_count = 0;
        for (const auto& pair : counter) {
            if (pair.second > max_count) {
                max_count = pair.second;
            }
        }
        std::vector<double> modes;
        for (const auto& pair : counter) {
            if (pair.second == max_count) {
                modes.push_back(pair.first);
            }
        }
        return modes;
    }
};