#include <any>
#include <cstddef>
#include <stdexcept>
#include <typeinfo>
#include <utility>
#include <vector>

class MetricsCalculator2 {
public:
    class Tuple {
    private:
        std::vector<int> list;
        int totalNum;

    public:
        Tuple(std::vector<int> list, int totalNum)
            : list(std::move(list)), totalNum(totalNum) {}

        std::vector<int>& getList() { return list; }
        const std::vector<int>& getList() const { return list; }
        int getTotalNum() const { return totalNum; }
    };

    static double mrr(const std::any& data) {
        if (data.type() != typeid(Tuple) &&
            data.type() != typeid(std::vector<Tuple>)) {
            throw std::invalid_argument(
                "the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple");
        }

        if (data.type() == typeid(Tuple)) {
            return mrrSingle(std::any_cast<const Tuple&>(data));
        } else {
            const auto& tupleList = std::any_cast<const std::vector<Tuple>&>(data);
            std::vector<double> separateResult;
            separateResult.reserve(tupleList.size());
            for (const auto& tuple : tupleList) {
                separateResult.push_back(mrrSingle(tuple));
            }
            return average(separateResult);
        }
    }

    static double map(const std::any& data) {
        if (data.type() != typeid(Tuple) &&
            data.type() != typeid(std::vector<Tuple>)) {
            throw std::invalid_argument(
                "the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple");
        }

        if (data.type() == typeid(Tuple)) {
            return mapSingle(std::any_cast<const Tuple&>(data));
        } else {
            const auto& tupleList = std::any_cast<const std::vector<Tuple>&>(data);
            std::vector<double> separateResult;
            separateResult.reserve(tupleList.size());
            for (const auto& tuple : tupleList) {
                separateResult.push_back(mapSingle(tuple));
            }
            return average(separateResult);
        }
    }

private:
    static double mrrSingle(const Tuple& tuple) {
        const auto& subList = tuple.getList();
        int totalNum = tuple.getTotalNum();

        if (totalNum == 0) {
            return 0.0;
        }

        for (std::size_t i = 0; i < subList.size(); ++i) {
            if (subList[i] == 1) {
                return 1.0 / (i + 1);
            }
        }
        return 0.0;
    }

    static double mapSingle(const Tuple& tuple) {
        const auto& subList = tuple.getList();
        int totalNum = tuple.getTotalNum();

        if (totalNum == 0) {
            return 0.0;
        }

        double ap = 0.0;
        int count = 0;
        for (std::size_t i = 0; i < subList.size(); ++i) {
            if (subList[i] == 1) {
                ++count;
                ap += count / (i + 1.0);
            }
        }
        return ap / totalNum;
    }

    static double average(const std::vector<double>& values) {
        if (values.empty()) {
            return 0.0;
        }
        double sum = 0.0;
        for (double v : values) {
            sum += v;
        }
        return sum / values.size();
    }
};