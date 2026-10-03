#include <vector>
#include <numeric>
#include <algorithm>
#include <cmath>
#include <limits>

class DataStatistics2 {
private:
    std::vector<double> data;

public:
    // Constructor takes a vector of ints, converts each to double
    DataStatistics2(const std::vector<int>& input)
        : data(input.begin(), input.end()) {}

    // Sum of all elements
    double getSum() const {
        return std::accumulate(data.begin(), data.end(), 0.0);
    }

    // Minimum value; returns NaN if data is empty
    double getMin() const {
        if (data.empty()) {
            return std::numeric_limits<double>::quiet_NaN();
        }
        return *std::min_element(data.begin(), data.end());
    }

    // Maximum value; returns NaN if data is empty
    double getMax() const {
        if (data.empty()) {
            return std::numeric_limits<double>::quiet_NaN();
        }
        return *std::max_element(data.begin(), data.end());
    }

    // Population variance (average of squared deviations from the mean)
    double getVariance() const {
        if (data.empty()) {
            return std::numeric_limits<double>::quiet_NaN();
        }
        double mean = getSum() / static_cast<double>(data.size());
        double sumSqDiff = std::accumulate(
            data.begin(), data.end(), 0.0,
            [mean](double accum, double val) {
                double diff = val - mean;
                return accum + diff * diff;
            }
        );
        return sumSqDiff / static_cast<double>(data.size());
    }

    // Standard deviation (square root of population variance)
    double getStdDeviation() const {
        return std::sqrt(getVariance());
    }

    // Correlation placeholder; always returns 1.0
    double getCorrelation() const {
        return 1.0;
    }
};