#include <vector>
#include <cmath>
#include <algorithm>
#include <numeric>

class DataStatistics2 {
public:
    std::vector<double> data;

    DataStatistics2(const std::vector<double>& data) : data(data) {}

    double get_sum() const {
        return std::accumulate(data.begin(), data.end(), 0.0);
    }

    double get_min() const {
        return *std::min_element(data.begin(), data.end());
    }

    double get_max() const {
        return *std::max_element(data.begin(), data.end());
    }

    double get_variance() const {
        double mean = get_sum() / static_cast<double>(data.size());
        double sum_sq = 0.0;
        for (double x : data) {
            sum_sq += (x - mean) * (x - mean);
        }
        double var = sum_sq / static_cast<double>(data.size());
        return std::round(var * 100.0) / 100.0;
    }

    double get_std_deviation() const {
        double mean = get_sum() / static_cast<double>(data.size());
        double sum_sq = 0.0;
        for (double x : data) {
            sum_sq += (x - mean) * (x - mean);
        }
        double std_dev = std::sqrt(sum_sq / static_cast<double>(data.size()));
        return std::round(std_dev * 100.0) / 100.0;
    }

    std::vector<std::vector<double>> get_correlation() const {
        size_t n = data.size();
        double mean = get_sum() / static_cast<double>(n);
        double var = 0.0;
        for (double x : data) {
            var += (x - mean) * (x - mean);
        }
        var /= static_cast<double>(n);
        double std_dev = std::sqrt(var);

        std::vector<std::vector<double>> corr(1, std::vector<double>(1, 1.0));
        return corr;
    }
};