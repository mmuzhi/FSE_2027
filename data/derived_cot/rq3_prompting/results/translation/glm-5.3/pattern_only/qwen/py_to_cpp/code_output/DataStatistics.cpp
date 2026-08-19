#include <vector>
#include <numeric>
#include <algorithm>
#include <cmath>
#include <unordered_map>

class DataStatistics {
public:
    double mean(const std::vector<double>& data) const {
        double sum = std::accumulate(data.begin(), data.end(), 0.0);
        return std::round((sum / static_cast<double>(data.size())) * 100.0) / 100.0;
    }

    double median(std::vector<double> data) const {
        std::sort(data.begin(), data.end());
        std::size_t n = data.size();
        if (n % 2 == 0) {
            std::size_t middle = n / 2;
            return std::round(((data[middle - 1] + data[middle]) / 2.0) * 100.0) / 100.0;
        } else {
            std::size_t middle = n / 2;
            return data[middle];  // odd case: returned un-rounded, as in Python
        }
    }

    std::vector<double> mode(const std::vector<double>& data) const {
        // Counter with insertion (first-occurrence) order preserved, as in Python
        std::unordered_map<double, int> counter;
        std::vector<double> order;
        for (double x : data) {
            auto it = counter.find(x);
            if (it == counter.end()) {
                counter[x] = 1;
                order.push_back(x);
            } else {
                it->second += 1;
            }
        }
        int mode_count = 0;
        for (const auto& kv : counter) {
            if (kv.second > mode_count) mode_count = kv.second;
        }
        std::vector<double> result;
        for (double x : order) {
            if (counter[x] == mode_count) result.push_back(x);
        }
        return result;
    }
};