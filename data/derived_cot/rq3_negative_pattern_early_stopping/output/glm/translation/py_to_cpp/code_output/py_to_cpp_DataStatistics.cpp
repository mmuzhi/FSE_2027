#include <vector>
#include <algorithm>
#include <numeric>
#include <unordered_map>
#include <cmath>
#include <stdexcept>

class DataStatistics {
public:
    double mean(const std::vector<double>& data) {
        if (data.empty()) {
            throw std::runtime_error("Division by zero");
        }
        double sum = std::accumulate(data.begin(), data.end(), 0.0);
        return std::round(sum / data.size() * 100.0) / 100.0;
    }

    double median(const std::vector<double>& data) {
        if (data.empty()) {
            throw std::runtime_error("Empty data");
        }
        std::vector<double> sorted_data = data;
        std::sort(sorted_data.begin(), sorted_data.end());
        int n = sorted_data.size();
        if (n % 2 == 0) {
            int middle = n / 2;
            return std::round((sorted_data[middle - 1] + sorted_data[middle]) / 2.0 * 100.0) / 100.0;
        } else {
            int middle = n / 2;
            return sorted_data[middle];
        }
    }

    std::vector<double> mode(const std::vector<double>& data) {
        if (data.empty()) {
            throw std::runtime_error("Empty data");
        }
        std::unordered_map<double, int> counter;
        std::vector<double> keys;
        
        // Count frequencies while preserving insertion order (like Python 3.7+ dict)
        for (double x : data) {
            if (counter.find(x) == counter.end()) {
                keys.push_back(x);
            }
            counter[x]++;
        }
        
        int mode_count = 0;
        for (const auto& pair : counter) {
            if (pair.second > mode_count) {
                mode_count = pair.second;
            }
        }
        
        std::vector<double> res;
        for (double x : keys) {
            if (counter[x] == mode_count) {
                res.push_back(x);
            }
        }
        
        return res;
    }
};