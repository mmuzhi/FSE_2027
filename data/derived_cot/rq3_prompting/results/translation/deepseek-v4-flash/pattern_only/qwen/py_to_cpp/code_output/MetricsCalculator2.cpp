#include <vector>
#include <utility>
#include <tuple>
#include <type_traits>
#include <stdexcept>
#include <numeric>

class MetricsCalculator2 {
public:
    using PredictionList = std::vector<int>;
    using SingleInput = std::pair<PredictionList, int>;
    using SingleTuple = std::tuple<PredictionList, int>;
    using MultiInput = std::vector<SingleInput>;
    using MultiTuple = std::vector<SingleTuple>;
    using Result = std::pair<double, std::vector<double>>;

private:
    static const PredictionList& get_sub_list(const SingleInput& data) { return data.first; }
    static int get_total_num(const SingleInput& data) { return data.second; }
    static const PredictionList& get_sub_list(const SingleTuple& data) { return std::get<0>(data); }
    static int get_total_num(const SingleTuple& data) { return std::get<1>(data); }

    static double compute_mrr_single(const PredictionList& sub_list, int total_num) {
        if (total_num == 0) return 0.0;
        for (size_t i = 0; i < sub_list.size(); ++i) {
            if (sub_list[i] > 0) {
                return 1.0 / static_cast<double>(i + 1);
            }
        }
        return 0.0;
    }

    static double compute_map_single(const PredictionList& sub_list, int total_num) {
        if (total_num == 0) return 0.0;
        double sum = 0.0;
        int count = 1;
        for (size_t i = 0; i < sub_list.size(); ++i) {
            if (sub_list[i] != 0) {
                sum += static_cast<double>(count) / static_cast<double>(i + 1);
                ++count;
            }
        }
        return sum / static_cast<double>(total_num);
    }

public:
    template<typename T>
    static Result mrr(const T& data) {
        using U = std::decay_t<T>;
        if constexpr (std::is_same_v<U, std::tuple<>>) {
            return {0.0, {0.0}};
        } else if constexpr (std::is_same_v<U, SingleInput> || std::is_same_v<U, SingleTuple>) {
            double mr = compute_mrr_single(get_sub_list(data), get_total_num(data));
            return {mr, {mr}};
        } else if constexpr (std::is_same_v<U, MultiInput> || std::is_same_v<U, MultiTuple>) {
            std::vector<double> separate_result;
            separate_result.reserve(data.size());
            for (const auto& item : data) {
                separate_result.push_back(compute_mrr_single(get_sub_list(item), get_total_num(item)));
            }
            if (separate_result.empty()) {
                return {0.0, {0.0}};
            }
            double sum = std::accumulate(separate_result.begin(), separate_result.end(), 0.0);
            return {sum / separate_result.size(), separate_result};
        } else {
            throw std::invalid_argument("the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple");
        }
    }

    template<typename T>
    static Result map(const T& data) {
        using U = std::decay_t<T>;
        if constexpr (std::is_same_v<U, std::tuple<>>) {
            return {0.0, {0.0}};
        } else if constexpr (std::is_same_v<U, SingleInput> || std::is_same_v<U, SingleTuple>) {
            double ap = compute_map_single(get_sub_list(data), get_total_num(data));
            return {ap, {ap}};
        } else if constexpr (std::is_same_v<U, MultiInput> || std::is_same_v<U, MultiTuple>) {
            std::vector<double> separate_result;
            separate_result.reserve(data.size());
            for (const auto& item : data) {
                separate_result.push_back(compute_map_single(get_sub_list(item), get_total_num(item)));
            }
            if (separate_result.empty()) {
                return {0.0, {0.0}};
            }
            double sum = std::accumulate(separate_result.begin(), separate_result.end(), 0.0);
            return {sum / separate_result.size(), separate_result};
        } else {
            throw std::invalid_argument("the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple");
        }
    }
};