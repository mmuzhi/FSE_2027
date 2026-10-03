#include <vector>
#include <utility>

using Query = std::pair<std::vector<int>, int>;

static std::pair<double, std::vector<double>> mrr(const Query& data) {
    if (data.second == 0) {
        return std::make_pair(0.0, std::vector<double>{0.0});
    }

    std::vector<double> reciprocal_ranks;
    reciprocal_ranks.reserve(data.first.size());
    for (size_t i = 0; i < data.first.size(); ++i) {
        reciprocal_ranks.push_back(1.0 / (i + 1));
    }

    double mr = 0.0;
    for (size_t i = 0; i < data.first.size(); ++i) {
        if (data.first[i] == 1) {
            mr = reciprocal_ranks[i];
            break;
        }
    }

    return std::make_pair(mr, std::vector<double>{mr});
}

static std::pair<double, std::vector<double>> mrr(const std::vector<Query>& data) {
    if (data.empty()) {
        return std::make_pair(0.0, std::vector<double>{0.0});
    }

    std::vector<double> separate_result;
    for (const auto& query : data) {
        auto result = mrr(query);
        separate_result.push_back(result.first);
    }

    double average = 0.0;
    for (double val : separate_result) {
        average += val;
    }
    average /= separate_result.size();

    return std::make_pair(average, separate_result);
}

static std::pair<double, std::vector<double>> map(const Query& data) {
    if (data.second == 0) {
        return std::make_pair(0.0, std::vector<double>{0.0});
    }

    std::vector<double> reciprocal_ranks;
    reciprocal_ranks.reserve(data.first.size());
    for (size_t i = 0; i < data.first.size(); ++i) {
        reciprocal_ranks.push_back(1.0 / (i + 1));
    }

    double current_count = 1.0;
    double ap_sum = 0.0;
    for (size_t i = 0; i < data.first.size(); ++i) {
        if (data.first[i] == 1) {
            ap_sum += current_count * reciprocal_ranks[i];
            current_count += 1.0;
        }
    }

    double ap = ap_sum / data.second;
    return std::make_pair(ap, std::vector<double>{ap});
}

static std::pair<double, std::vector<double>> map(const std::vector<Query>& data) {
    if (data.empty()) {
        return std::make_pair(0.0, std::vector<double>{0.0});
    }

    std::vector<double> separate_result;
    for (const auto& query : data) {
        auto result = map(query);
        separate_result.push_back(result.first);
    }

    double average = 0.0;
    for (double val : separate_result) {
        average += val;
    }
    average /= separate_result.size();

    return std::make_pair(average, separate_result);
}