#include <algorithm>
#include <cmath>
#include <cstddef>
#include <map>
#include <stdexcept>
#include <utility>
#include <vector>

class DataStatistics {
public:
    // Calculate the average value of a group of data, accurate to two digits
    // after the decimal separator.
    double mean(const std::vector<double>& data) const {
        if (data.empty()) {
            // Python: sum(data) / len(data) raises ZeroDivisionError on empty input.
            throw std::runtime_error("division by zero");
        }
        double sum = 0.0;
        for (double value : data) {
            sum += value;
        }
        return round_to(sum / static_cast<double>(data.size()), 2);
    }

    // Calculate the median of a group of data, accurate to two digits after
    // the decimal separator.
    double median(const std::vector<double>& data) const {
        std::vector<double> sorted_data(data);  // sorted(data) does not mutate the input
        std::sort(sorted_data.begin(), sorted_data.end());
        const std::size_t n = sorted_data.size();
        const std::size_t middle = n / 2;
        if (n % 2 == 0) {
            if (n == 0) {
                // Python: sorted_data[middle - 1] == sorted_data[-1] raises IndexError.
                throw std::out_of_range("list index out of range");
            }
            return round_to((sorted_data[middle - 1] + sorted_data[middle]) / 2.0, 2);
        }
        // Odd length: Python returns the middle element unrounded.
        return sorted_data[middle];
    }

    // Calculate the mode of a set of data.
    std::vector<double> mode(const std::vector<double>& data) const {
        if (data.empty()) {
            // Python: max() on the empty counter raises ValueError.
            throw std::invalid_argument("max() arg is an empty sequence");
        }

        // Counter equivalent: counts per value; first-occurrence order is kept
        // because Python dicts/Counters preserve insertion order.
        std::map<double, int> counter;
        std::vector<double> order;
        for (double value : data) {
            std::pair<std::map<double, int>::iterator, bool> inserted =
                counter.insert(std::make_pair(value, 0));
            if (inserted.second) {
                order.push_back(value);
            }
            ++inserted.first->second;
        }

        int mode_count = 0;
        for (const auto& entry : counter) {
            mode_count = std::max(mode_count, entry.second);
        }

        std::vector<double> result;
        for (double value : order) {
            if (counter[value] == mode_count) {
                result.push_back(value);
            }
        }
        return result;
    }

private:
    // Python-style round(): ties round to even, at the given number of digits.
    static double round_to(double value, int digits) {
        const double scale = std::pow(10.0, static_cast<double>(digits));
        return std::nearbyint(value * scale) / scale;
    }
};