#include <vector>
#include <stdexcept>
#include <algorithm>
#include <cmath>
#include <unordered_map>

class DataStatistics {
public:
    double mean(const std::vector<double>& data) const {
        if (data.empty()) {
            // Python: sum(data) / len(data) raises ZeroDivisionError on empty input
            throw std::runtime_error("division by zero");
        }
        double sum = 0.0;
        for (double x : data) sum += x;
        return roundTo2(sum / static_cast<double>(data.size()));
    }

    double median(const std::vector<double>& data) const {
        if (data.empty()) {
            // Python: sorted_data[-1] raises IndexError on empty input
            throw std::out_of_range("index out of range");
        }
        std::vector<double> sorted_data(data);
        std::sort(sorted_data.begin(), sorted_data.end());
        std::size_t n = sorted_data.size();
        std::size_t middle = n / 2;
        if (n % 2 == 0) {
            return roundTo2((sorted_data[middle - 1] + sorted_data[middle]) / 2.0);
        } else {
            // Odd case returns the middle element unrounded (as in Python)
            return sorted_data[middle];
        }
    }

    std::vector<double> mode(const std::vector<double>& data) const {
        // Emulates collections.Counter: counts by value, preserving
        // first-occurrence (insertion) order.
        std::vector<double> values;
        std::vector<long long> counts;
        std::unordered_map<double, std::size_t> index;
        for (double x : data) {
            auto it = index.find(x);
            if (it == index.end()) {
                index[x] = values.size();
                values.push_back(x);
                counts.push_back(1);
            } else {
                counts[it->second]++;
            }
        }
        if (values.empty()) {
            // Python: max() on empty sequence raises ValueError
            throw std::invalid_argument("max() arg is an empty sequence");
        }
        long long mode_count = *std::max_element(counts.begin(), counts.end());
        std::vector<double> result;
        for (std::size_t i = 0; i < values.size(); ++i) {
            if (counts[i] == mode_count) result.push_back(values[i]);
        }
        return result;
    }

private:
    static double roundTo2(double value) {
        // Python's round() uses round-half-to-even; std::nearbyint with the
        // default FE_TONEAREST rounding mode matches that behavior
        // (unlike std::round, which rounds half away from zero).
        return std::nearbyint(value * 100.0) / 100.0;
    }
};