#include <vector>
#include <algorithm>
#include <map>
#include <stdexcept>
#include <cmath>

class DataStatistics {
public:
    double mean(const std::vector<double>& data) {
        if (data.empty()) {
            throw std::runtime_error("DataStatistics: empty data set");
        }
        double sum = 0.0;
        for (double d : data) {
            sum += d;
        }
        double average = sum / data.size();
        return std::round(average * 100.0) / 100.0;
    }

    double median(std::vector<double> data) {
        if (data.empty()) {
            throw std::runtime_error("DataStatistics: empty data set");
        }
        std::sort(data.begin(), data.end());
        size_t n = data.size();
        if (n % 2 == 0) {
            size_t middle = n / 2;
            double average = (data[middle - 1] + data[middle]) / 2.0;
            return std::round(average * 100.0) / 100.0;
        } else {
            size_t middle = n / 2;
            return data[middle];
        }
    }

    std::vector<double> mode(std::vector<double> data) {
        if (data.empty()) {
            throw std::runtime_error("DataStatistics: empty data set");
        }
        std::map<double, int> counter;
        for (double d : data) {
            counter[d]++;
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