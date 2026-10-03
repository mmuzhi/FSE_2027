#include <vector>
#include <iostream>
#include <stdexcept>
#include <cmath>
#include <variant>
#include <numeric>
#include <algorithm>

class Tuple {
private:
    std::vector<int> list;
    int totalNum;

public:
    Tuple(std::vector<int> list, int totalNum) : list(std::move(list)), totalNum(totalNum) {}

    const std::vector<int>& getList() const { return list; }
    int getTotalNum() const { return totalNum; }
};

using Input = std::variant<Tuple, std::vector<Tuple>>;

double mrr(Input input) {
    if (input.index() != 0 && input.index() != 1) {
        throw std::invalid_argument("the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple");
    }

    if (std::holds_alternative<Tuple>(input)) {
        const Tuple& tuple = std::get<Tuple>(input);
        const auto& subList = tuple.getList();
        int totalNum = tuple.getTotalNum();

        if (totalNum == 0) {
            return 0.0;
        }

        double mr = 0.0;
        for (size_t i = 0; i < subList.size(); ++i) {
            if (subList[i] == 1) {
                mr = 1.0 / (i + 1);
                break;
            }
        }
        return mr;
    } else {
        const auto& tupleList = std::get<std::vector<Tuple>>(input);
        std::vector<double> separateResult;

        for (const Tuple& tuple : tupleList) {
            const auto& subList = tuple.getList();
            int totalNum = tuple.getTotalNum();

            if (totalNum == 0) {
                separateResult.push_back(0.0);
            } else {
                double mr = 0.0;
                for (size_t i = 0; i < subList.size(); ++i) {
                    if (subList[i] == 1) {
                        mr = 1.0 / (i + 1);
                        break;
                    }
                }
                separateResult.push_back(mr);
            }
        }

        if (separateResult.empty()) {
            return 0.0;
        }
        return std::accumulate(separateResult.begin(), separateResult.end(), 0.0) / separateResult.size();
    }
}

double map(Input input) {
    if (input.index() != 0 && input.index() != 1) {
        throw std::invalid_argument("the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple");
    }

    if (std::holds_alternative<Tuple>(input)) {
        const Tuple& tuple = std::get<Tuple>(input);
        const auto& subList = tuple.getList();
        int totalNum = tuple.getTotalNum();

        if (totalNum == 0) {
            return 0.0;
        }

        double ap = 0.0;
        int count = 0;
        for (size_t i = 0; i < subList.size(); ++i) {
            if (subList[i] == 1) {
                ++count;
                ap += static_cast<double>(count) / (i + 1.0);
            }
        }
        return ap / totalNum;
    } else {
        const auto& tupleList = std::get<std::vector<Tuple>>(input);
        std::vector<double> separateResult;

        for (const Tuple& tuple : tupleList) {
            const auto& subList = tuple.getList();
            int totalNum = tuple.getTotalNum();

            if (totalNum == 0) {
                separateResult.push_back(0.0);
            } else {
                double ap = 0.0;
                int count = 0;
                for (size_t i = 0; i < subList.size(); ++i) {
                    if (subList[i] == 1) {
                        ++count;
                        ap += static_cast<double>(count) / (i + 1.0);
                    }
                }
                separateResult.push_back(ap / totalNum);
            }
        }

        if (separateResult.empty()) {
            return 0.0;
        }
        return std::accumulate(separateResult.begin(), separateResult.end(), 0.0) / separateResult.size();
    }
}