#include <vector>
#include <numeric>
#include <algorithm>
#include <stdexcept>
#include <utility>

class MetricsCalculator2 {
public:
    // Helper: compute MRR for a single (sub_list, total_num)
    static double compute_mrr_single(const std::vector<int>& sub_list, int total_num) {
        if (total_num == 0 || sub_list.empty()) {
            return 0.0;
        }
        for (size_t i = 0; i < sub_list.size(); ++i) {
            if (sub_list[i] == 1) {
                return 1.0 / (i + 1.0);
            }
        }
        return 0.0;
    }

    // Helper: compute MAP for a single (sub_list, total_num)
    static double compute_map_single(const std::vector<int>& sub_list, int total_num) {
        if (total_num == 0 || sub_list.empty()) {
            return 0.0;
        }
        double sum = 0.0;
        int correct_count = 0;
        for (size_t i = 0; i < sub_list.size(); ++i) {
            if (sub_list[i] == 1) {
                correct_count++;
                sum += static_cast<double>(correct_count) / (i + 1.0);
            }
        }
        return sum / total_num;
    }

    // Version for a list of (sub_list, total_num)
    static std::pair<double, std::vector<double>> mrr(
        const std::vector<std::pair<std::vector<int>, int>>& data) {
        if (data.empty()) {
            return {0.0, std::vector<double>{0.0}};
        }
        std::vector<double> results;
        results.reserve(data.size());
        for (const auto& pair : data) {
            results.push_back(compute_mrr_single(pair.first, pair.second));
        }
        double mean = std::accumulate(results.begin(), results.end(), 0.0) / results.size();
        return {mean, results};
    }

    // Overload for a single tuple
    static std::pair<double, std::vector<double>> mrr(
        const std::pair<std::vector<int>, int>& data) {
        std::vector<std::pair<std::vector<int>, int>> vec = {data};
        return mrr(vec);
    }

    static std::pair<double, std::vector<double>> map(
        const std::vector<std::pair<std::vector<int>, int>>& data) {
        if (data.empty()) {
            return {0.0, std::vector<double>{0.0}};
        }
        std::vector<double> results;
        results.reserve(data.size());
        for (const auto& pair : data) {
            results.push_back(compute_map_single(pair.first, pair.second));
        }
        double mean = std::accumulate(results.begin(), results.end(), 0.0) / results.size();
        return {mean, results};
    }

    static std::pair<double, std::vector<double>> map(
        const std::pair<std::vector<int>, int>& data) {
        std::vector<std::pair<std::vector<int>, int>> vec = {data};
        return map(vec);
    }
};