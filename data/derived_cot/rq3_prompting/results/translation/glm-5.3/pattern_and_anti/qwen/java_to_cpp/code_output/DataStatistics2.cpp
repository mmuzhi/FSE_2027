#pragma once

#include <cmath>
#include <limits>
#include <vector>

class DataStatistics2 {
public:
    explicit DataStatistics2(const std::vector<int>& data)
        : data_(data.begin(), data.end()) {}

    double getSum() const {
        double sum = 0.0;
        for (double v : data_) {
            sum += v;
        }
        return sum;
    }

    double getMin() const {
        if (data_.empty()) {
            return std::numeric_limits<double>::quiet_NaN();
        }
        double m = data_[0];
        for (double v : data_) {
            if (v < m) m = v;
        }
        return m;
    }

    double getMax() const {
        if (data_.empty()) {
            return std::numeric_limits<double>::quiet_NaN();
        }
        double m = data_[0];
        for (double v : data_) {
            if (v > m) m = v;
        }
        return m;
    }

    double getVariance() const {
        if (data_.empty()) {
            return std::numeric_limits<double>::quiet_NaN();
        }
        double mean = getSum() / static_cast<double>(data_.size());
        double sqSum = 0.0;
        for (double v : data_) {
            sqSum += (v - mean) * (v - mean);
        }
        return sqSum / static_cast<double>(data_.size());
    }

    double getStdDeviation() const {
        return std::sqrt(getVariance());
    }

    double getCorrelation() const {
        return 1.0;
    }

private:
    std::vector<double> data_;
};