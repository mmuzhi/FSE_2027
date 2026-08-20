#include <algorithm>
#include <cmath>
#include <limits>
#include <numeric>
#include <vector>

class DataStatistics2 {
private:
    std::vector<double> data;

public:
    explicit DataStatistics2(const std::vector<int>& data)
        : data(data.begin(), data.end()) {}

    double getSum() const {
        // Matches DoubleStream.sum(): identity 0.0, plain left-to-right addition.
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
        // Empty input: Java's average() on an empty stream yields orElse(NaN).
        if (data.empty()) {
            return std::numeric_limits<double>::quiet_NaN();
        }
        const double count = static_cast<double>(data.size());
        const double mean = getSum() / count;
        double sumOfSquaredDeviations = 0.0;
        for (double value : data) {
            const double deviation = value - mean;
            sumOfSquaredDeviations += deviation * deviation;
        }
        // Same as average(): left-to-right sum divided by element count.
        return sumOfSquaredDeviations / count;
    }

    double getStdDeviation() const {
        return std::sqrt(getVariance());
    }

    double getCorrelation() const {
        return 1.0;
    }
};