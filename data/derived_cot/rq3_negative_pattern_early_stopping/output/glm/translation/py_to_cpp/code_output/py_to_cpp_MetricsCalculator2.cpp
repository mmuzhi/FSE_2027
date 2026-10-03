#include <vector>
#include <variant>
#include <stdexcept>
#include <numeric>
#include <utility>

class MetricsCalculator2 {
public:
    using SingleData = std::pair<std::vector<int>, int>;
    using MultiData = std::vector<SingleData>;
    using InputData = std::variant<SingleData, MultiData>;
    using Result = std::pair<double, std::vector<double>>;

    static Result mrr(const InputData& data) {
        if (std::holds_alternative<SingleData>(data)) {
            const auto& [sub_list, total_num] = std::get<SingleData>(data);
            if (total_num == 0) {
                return {0.0, {0.0}};
            }
            double mr = 0.0;
            for (size_t i = 0; i < sub_list.size(); ++i) {
                double val = sub_list[i] * (1.0 / (static_cast<double>(i) + 1.0));
                if (val > 0.0) {
                    mr = val;
                    break;
                }
            }
            return {mr, {mr}};
        } else if (std::holds_alternative<MultiData>(data)) {
            const auto& multi = std::get<MultiData>(data);
            if (multi.empty()) {
                return {0.0, {0.0}};
            }
            std::vector<double> separate_result;
            for (const auto& [sub_list, total_num] : multi) {
                double mr = 0.0;
                if (total_num != 0) {
                    for (size_t i = 0; i < sub_list.size(); ++i) {
                        double val = sub_list[i] * (1.0 / (static_cast<double>(i) + 1.0));
                        if (val > 0.0) {
                            mr = val;
                            break;
                        }
                    }
                }
                separate_result.push_back(mr);
            }
            double mean = std::accumulate(separate_result.begin(), separate_result.end(), 0.0) / static_cast<double>(separate_result.size());
            return {mean, separate_result};
        }
        throw std::runtime_error("the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple");
    }

    static Result map(const InputData& data) {
        if (std::holds_alternative<SingleData>(data)) {
            const auto& [sub_list, total_num] = std::get<SingleData>(data);
            if (total_num == 0) {
                return {0.0, {0.0}};
            }
            std::vector<double> right_ranking_list;
            int count = 1;
            for (int t : sub_list) {
                if (t == 0) {
                    right_ranking_list.push_back(0.0);
                } else {
                    right_ranking_list.push_back(static_cast<double>(count));
                    count++;
                }
            }
            double ap = 0.0;
            for (size_t i = 0; i < right_ranking_list.size(); ++i) {
                ap += right_ranking_list[i] * (1.0 / (static_cast<double>(i) + 1.0));
            }
            ap /= static_cast<double>(total_num);
            return {ap, {ap}};
        } else if (std::holds_alternative<MultiData>(data)) {
            const auto& multi = std::get<MultiData>(data);
            if (multi.empty()) {
                return {0.0, {0.0}};
            }
            std::vector<double> separate_result;
            for (const auto& [sub_list, total_num] : multi) {
                double ap = 0.0;
                if (total_num != 0) {
                    std::vector<double> right_ranking_list;
                    int count = 1;
                    for (int t : sub_list) {
                        if (t == 0) {
                            right_ranking_list.push_back(0.0);
                        } else {
                            right_ranking_list.push_back(static_cast<double>(count));
                            count++;
                        }
                    }
                    for (size_t i = 0; i < right_ranking_list.size(); ++i) {
                        ap += right_ranking_list[i] * (1.0 / (static_cast<double>(i) + 1.0));
                    }
                    ap /= static_cast<double>(total_num);
                }
                separate_result.push_back(ap);
            }
            double mean = std::accumulate(separate_result.begin(), separate_result.end(), 0.0) / static_cast<double>(separate_result.size());
            return {mean, separate_result};
        }
        throw std::runtime_error("the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple");
    }
};