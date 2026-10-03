#include <vector>
#include <cmath>
#include <limits>
#include <algorithm>
#include <numeric>

class DataStatistics2 {
private:
    std::vector<double> data;

public:
    explicit DataStatistics2(const std::vector<int>& data) {
        for (int i : data) {
            this->data.push_back(static_cast<double>(i));
        }
    }

    double getSum() const {
        if (data.empty()) {
            return 0.0;
        }
        return std::accumulate(data.begin(), data.end(), 0.0);
    }

    double getMin() const {
        if (data.empty()) {
            return std::numeric_limits<double>::quiet_NaN();
        }
        return *std::min_element(data.begin(), data.end());
    }

    double getMax() const {
        if (data.empty()) {
            return std::numeric_limits<double>::quiet_NaN();
        }
        return *std::max_element(data.begin(), data.end());
    }

    double getVariance() const {
        if (data.empty()) {
            return std::numeric_limits<double>::quiet_NaN();
        }
        double mean = getSum() / data.size();
        double sq_sum = 0.0;
        for (double val : data) {
            sq_sum += (val - mean) * (val - mean);
        }
        return sq_sum / data.size();
    }

    double getStdDeviation() const {
        double variance = getVariance();
        return std::sqrt(variance);
    }

    double getCorrelation() const {
        return 1.0;
    }
};