#include <vector>
#include <cmath>
#include <algorithm>
#include <numeric>
#include <stdexcept>
#include <limits>

class DataStatistics2 {
private:
    std::vector<double> data;

public:
    DataStatistics2(const std::vector<double>& data) : data(data) {}

    double get_sum() {
        if (data.empty()) {
            return 0.0;
        }
        return std::accumulate(data.begin(), data.end(), 0.0);
    }

    double get_min() {
        if (data.empty()) {
            throw std::runtime_error("Empty data: min is undefined");
        }
        return *std::min_element(data.begin(), data.end());
    }

    double get_max() {
        if (data.empty()) {
            throw std::runtime_error("Empty data: max is undefined");
        }
        return *std::max_element(data.begin(), data.end());
    }

    double get_variance() {
        if (data.empty()) {
            throw std::runtime_error("Empty data: variance is undefined");
        }
        double mean = get_sum() / data.size();
        double sq_diff_sum = 0.0;
        for (double d : data) {
            double diff = d - mean;
            sq_diff_sum += diff * diff;
        }
        double variance = sq_diff_sum / data.size();
        return std::round(variance * 100.0) / 100.0;
    }

    double get_std_deviation() {
        if (data.empty()) {
            throw std::runtime_error("Empty data: standard deviation is undefined");
        }
        double variance = get_variance();
        return std::sqrt(variance);
    }

    double get_correlation() {
        if (data.size() < 2) {
            throw std::runtime_error("Data must have at least two points for correlation");
        }
        return 1.0;
    }
};