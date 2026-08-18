#include <vector>
#include <utility>
#include <stdexcept>

class MetricsCalculator2 {
public:
    // ([1,0,...], total_num)
    using Entry  = std::pair<std::vector<int>, int>;
    // list of tuples
    using Data   = std::vector<Entry>;
    using Result = std::pair<double, std::vector<double>>;

    MetricsCalculator2() {}

    // Fallback for any other type: mirrors the Python type check exception
    template <typename T>
    static Result mrr(const T&) {
        throw std::runtime_error("the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple");
    }
    template <typename T>
    static Result map(const T&) {
        throw std::runtime_error("the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple");
    }

    // tuple case: data == (sub_list, total_num), len(data) != 0 always holds for a pair
    static Result mrr(const Entry& data) {
        const std::vector<int>& sub_list = data.first;
        int total_num = data.second;

        if (total_num == 0)
            return {0.0, {0.0}};

        // ranking_array = 1.0 / (arange(n) + 1); first positive sub_list[i] * ranking_array[i]
        double mr = 0.0;
        for (std::size_t i = 0; i < sub_list.size(); ++i) {
            double team = sub_list[i] * (1.0 / static_cast<double>(i + 1));
            if (team > 0) {
                mr = team;
                break;
            }
        }
        return {mr, {mr}};
    }

    // list case
    static Result mrr(const Data& data) {
        if (data.empty())
            return {0.0, {0.0}};

        std::vector<double> separate_result;
        separate_result.reserve(data.size());
        for (const Entry& item : data) {
            const std::vector<int>& sub_list = item.first;
            int total_num = item.second;

            double mr = 0.0;
            if (total_num != 0) {
                for (std::size_t i = 0; i < sub_list.size(); ++i) {
                    double team = sub_list[i] * (1.0 / static_cast<double>(i + 1));
                    if (team > 0) {
                        mr = team;
                        break;
                    }
                }
            }
            separate_result.push_back(mr);
        }
        return {mean(separate_result), separate_result};
    }

    // tuple case
    static Result map(const Entry& data) {
        const std::vector<int>& sub_list = data.first;
        int total_num = data.second;

        if (total_num == 0)
            return {0.0, {0.0}};

        // right_ranking_list: count of hits so far at hit positions, else 0
        double sum = 0.0;
        int count = 1;
        for (std::size_t i = 0; i < sub_list.size(); ++i) {
            double right = 0.0;
            if (sub_list[i] == 0) {
                right = 0.0;
            } else {
                right = static_cast<double>(count);
                count += 1;
            }
            sum += right * (1.0 / static_cast<double>(i + 1));
        }
        double ap = sum / static_cast<double>(total_num);
        return {ap, {ap}};
    }

    // list case
    static Result map(const Data& data) {
        if (data.empty())
            return {0.0, {0.0}};

        std::vector<double> separate_result;
        separate_result.reserve(data.size());
        for (const Entry& item : data) {
            const std::vector<int>& sub_list = item.first;
            int total_num = item.second;

            double ap = 0.0;
            if (total_num != 0) {
                double sum = 0.0;
                int count = 1;
                for (std::size_t i = 0; i < sub_list.size(); ++i) {
                    double right = 0.0;
                    if (sub_list[i] == 0) {
                        right = 0.0;
                    } else {
                        right = static_cast<double>(count);
                        count += 1;
                    }
                    sum += right * (1.0 / static_cast<double>(i + 1));
                }
                ap = sum / static_cast<double>(total_num);
            }
            separate_result.push_back(ap);
        }
        return {mean(separate_result), separate_result};
    }

private:
    // np.mean equivalent (never called on empty vector here)
    static double mean(const std::vector<double>& v) {
        double s = 0.0;
        for (double x : v) s += x;
        return s / static_cast<double>(v.size());
    }
};