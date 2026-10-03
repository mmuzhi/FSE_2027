#include <vector>
#include <numeric>
#include <cmath>
#include <algorithm>
#include <stdexcept>

class DataStatistics2 {
private:
    std::vector<double> data;
public:
    DataStatistics2(const std::vector<double>& input_data) : data(input_data) {}

    double get_sum() const {
        return std::accumulate(data.begin(), data.end(), 0.0);
    }

    double get_min() const {
        if (data.empty()) throw std::runtime_error("Data is empty");
        return *std::min_element(data.begin(), data.end());
    }

    double get_max() const {
        if (data.empty()) throw std::runtime_error("Data is empty");
        return *std::max_element(data.begin(), data.end());
    }

    double get_variance() const {
        if (data.empty()) throw std::runtime_error("Data is empty");
        double mean = get_sum() / data.size();
        double sq_sum = 0.0;
        for (double x : data) sq_sum += (x - mean) * (x - mean);
        double var = sq_sum / data.size();
        return std::round(var * 100.0) / 100.0;
    }

    double get_std_deviation() const {
        double var = get_variance();
        double stdev = std::sqrt(var);
        return std::round(stdev * 100.0) / 100.0;
    }

    std::vector<std::vector<double>> get_correlation() const {
        if (data.empty()) throw std::runtime_error("Data is empty");
        size_t n = data.size();
        double mean = get_sum() / n;
        double std_dev = std::sqrt(get_variance());
        if (std_dev == 0.0) {
            std::vector<std::vector<double>> corr(2, std::vector<double>(2, 1.0));
            return corr;
        }
        std::vector<double> normalized;
        normalized.reserve(n);
        for (double x : data) normalized.push_back((x - mean) / std_dev);
        double n_minus_1 = static_cast<double>(n) - 1.0;
        // correlation of data with itself -> 1.0 for off-diagonal as well
        std::vector<std::vector<double>> corr(2, std::vector<double>(2, 1.0));
        return corr;
    }
};