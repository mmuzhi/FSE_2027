#include <vector>
#include <utility>
#include <variant>
#include <stdexcept>
#include <numeric>

class MetricsCalculator2 {
public:
    // Input types: a single (list, total_num) "tuple", or a list of such tuples.
    // std::monostate represents an unsupported input type (triggers the exception).
    using Item = std::pair<std::vector<double>, int>;
    using Data = std::variant<std::monostate, Item, std::vector<Item>>;
    using Result = std::pair<double, std::vector<double>>;

    MetricsCalculator2() {}

    static Result mrr(const Data& data) {
        if (!std::holds_alternative<Item>(data) &&
            !std::holds_alternative<std::vector<Item>>(data)) {
            throw std::runtime_error(
                "the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple");
        }

        if (const auto* single = std::get_if<Item>(&data)) {
            const std::vector<double>& sub_list = single->first;
            const int total_num = single->second;
            if (total_num == 0) {
                return {0.0, {0.0}};
            }
            double mr = 0.0;
            for (std::size_t i = 0; i < sub_list.size(); ++i) {
                double team = sub_list[i] / static_cast<double>(i + 1);
                if (team > 0.0) {
                    mr = team;
                    break;
                }
            }
            return {mr, {mr}};
        }

        const std::vector<Item>& items = std::get<std::vector<Item>>(data);
        if (items.empty()) {
            return {0.0, {0.0}};
        }

        std::vector<double> separate_result;
        separate_result.reserve(items.size());
        for (const auto& entry : items) {
            const std::vector<double>& sub_list = entry.first;
            const int total_num = entry.second;

            double mr = 0.0;
            if (total_num != 0) {
                for (std::size_t i = 0; i < sub_list.size(); ++i) {
                    double team = sub_list[i] / static_cast<double>(i + 1);
                    if (team > 0.0) {
                        mr = team;
                        break;
                    }
                }
            }
            separate_result.push_back(mr);
        }
        double mean = std::accumulate(separate_result.begin(), separate_result.end(), 0.0) /
                      static_cast<double>(separate_result.size());
        return {mean, separate_result};
    }

    static Result map(const Data& data) {
        if (!std::holds_alternative<Item>(data) &&
            !std::holds_alternative<std::vector<Item>>(data)) {
            throw std::runtime_error(
                "the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple");
        }

        if (const auto* single = std::get_if<Item>(&data)) {
            const std::vector<double>& sub_list = single->first;
            const int total_num = single->second;
            if (total_num == 0) {
                return {0.0, {0.0}};
            }
            double ap = compute_ap(sub_list, total_num);
            return {ap, {ap}};
        }

        const std::vector<Item>& items = std::get<std::vector<Item>>(data);
        if (items.empty()) {
            return {0.0, {0.0}};
        }

        std::vector<double> separate_result;
        separate_result.reserve(items.size());
        for (const auto& entry : items) {
            const std::vector<double>& sub_list = entry.first;
            const int total_num = entry.second;

            double ap = 0.0;
            if (total_num != 0) {
                ap = compute_ap(sub_list, total_num);
            }
            separate_result.push_back(ap);
        }
        double mean = std::accumulate(separate_result.begin(), separate_result.end(), 0.0) /
                      static_cast<double>(separate_result.size());
        return {mean, separate_result};
    }

private:
    static double compute_ap(const std::vector<double>& sub_list, int total_num) {
        // ranking_array = 1 / (i + 1)
        // right_ranking_list: cumulative count for non-zero entries, 0 otherwise
        // ap = sum(right_ranking_list * ranking_array) / total_num
        std::vector<double> right_ranking_list;
        right_ranking_list.reserve(sub_list.size());
        int count = 1;
        for (double t : sub_list) {
            if (t == 0.0) {
                right_ranking_list.push_back(0.0);
            } else {
                right_ranking_list.push_back(static_cast<double>(count));
                ++count;
            }
        }
        double sum = 0.0;
        for (std::size_t i = 0; i < right_ranking_list.size(); ++i) {
            sum += right_ranking_list[i] / static_cast<double>(i + 1);
        }
        return sum / static_cast<double>(total_num);
    }
};