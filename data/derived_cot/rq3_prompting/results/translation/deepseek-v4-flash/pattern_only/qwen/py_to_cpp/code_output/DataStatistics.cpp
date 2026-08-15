#include <vector>
#include <algorithm>
#include <cmath>
#include <unordered_map>
#include <stdexcept>

class DataStatistics {
public:
    template<typename T>
    double mean(const std::vector<T>& data) {
        if (data.empty()) {
            throw std::invalid_argument("empty data");
        }
        double sum = 0.0;
        for (const auto& x : data) {
            sum += static_cast<double>(x);
        }
        return round_to_2(sum / data.size());
    }

    template<typename T>
    double median(const std::vector<T>& data) {
        if (data.empty()) {
            throw std::out_of_range("empty data");
        }
        std::vector<T> sorted_data = data;
        std::sort(sorted_data.begin(), sorted_data.end());
        size_t n = sorted_data.size();

        if (n % 2 == 0) {
            size_t middle = n / 2;
            double avg = (static_cast<double>(sorted_data[middle - 1]) +
                          static_cast<double>(sorted_data[middle])) / 2.0;
            return round_to_2(avg);
        } else {
            size_t middle = n / 2;
            return static_cast<double>(sorted_data[middle]);
        }
    }

    template<typename T>
    std::vector<T> mode(const std::vector<T>& data) {
        if (data.empty()) {
            throw std::invalid_argument("empty data");
        }

        std::unordered_map<T, size_t> counts;
        std::vector<T> order;

        for (const auto& x : data) {
            if (counts.find(x) == counts.end()) {
                counts[x] = 1;
                order.push_back(x);
            } else {
                ++counts[x];
            }
        }

        size_t max_count = 0;
        for (const auto& p : counts) {
            if (p.second > max_count) {
                max_count = p.second;
            }
        }

        std::vector<T> result;
        for (const auto& x : order) {
            if (counts[x] == max_count) {
                result.push_back(x);
            }
        }

        return result;
    }

private:
    static double round_to_2(double x) {
        return std::nearbyint(x * 100.0) / 100.0;
    }
};