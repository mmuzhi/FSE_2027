#ifndef DATA_STATISTICS2_H
#define DATA_STATISTICS2_H

#include <vector>
#include <cmath>
#include <limits>

class DataStatistics2 {
private:
    std::vector<double> data;

public:
    explicit DataStatistics2(const std::vector<int>& data_)
        : data(data_.begin(), data_.end()) {}

    double getSum() const {
        double sum = 0.0;
        for (double v : data) {
            sum += v;
        }
        return sum;
    }

    double getMin() const {
        if (data.empty()) {
            return std::numeric_limits<double>::quiet_NaN();
        }
        double m = data[0];
        for (double v : data) {
            if (v < m) m = v;
        }
        return m;
    }

    double getMax() const {
        if (data.empty()) {
            return std::numeric_limits<double>::quiet_NaN();
        }
        double m = data[0];
        for (double v : data) {
            if (v > m) m = v;
        }
        return m;
    }

    double getVariance() const {
        double mean = getSum() / static_cast<double>(data.size());
        double sumSq = 0.0;
        for (double v : data) {
            double d = v - mean;
            sumSq += d * d;
        }
        if (data.empty()) {
            return std::numeric_limits<double>::quiet_NaN();
        }
        return sumSq / static_cast<double>(data.size());
    }

    double getStdDeviation() const {
        return std::sqrt(getVariance());
    }

    double getCorrelation() const {
        return 1.0;
    }
};

#endif // DATA_STATISTICS2_H