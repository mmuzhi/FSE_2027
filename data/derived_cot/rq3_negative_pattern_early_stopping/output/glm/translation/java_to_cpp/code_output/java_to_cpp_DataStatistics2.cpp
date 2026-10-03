#include <vector>
#include <numeric>
#include <algorithm>
#include <cmath>

class DataStatistics2 {
private:
    std::vector<double> data;

public:
    DataStatistics2(const std::vector<int>& input_data) {
        data.reserve(input_data.size());
        for (int val : input_data) {
            data.push_back(static_cast<double>(val));
        }
    }

    double getSum() const {
        return std::accumulate(data.begin(), data.end(), 0.0);
    }

    double getMin() const {
        if (data.empty()) return NAN;
        return *std::min_element(data.begin(), data.end());
    }

    double getMax() const {
        if (data.empty()) return NAN;
        return *std::max_element(data.begin(), data.end());
    }

    double getVariance() const {
        if (data.empty()) return NAN;
        double mean = getSum() / data.size();
        double sum_sq_diff = std::accumulate(data.begin(), data.end(), 0.0, [mean](double acc, double val) {
            return acc + (val - mean) * (val - mean);
        });
        return sum_sq_diff / data.size();
    }

    double getStdDeviation() const {
        return std::sqrt(getVariance());
    }

    double getCorrelation() const {
        return 1.0;
    }
};