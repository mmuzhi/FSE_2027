#include <cstddef>
#include <stdexcept>
#include <utility>
#include <variant>
#include <vector>

namespace org::example {

class MetricsCalculator2 {
public:
    class Tuple {
    public:
        Tuple(std::vector<int> list, int totalNum)
            : list_(std::move(list)), totalNum_(totalNum) {}

        const std::vector<int>& getList() const { return list_; }
        int getTotalNum() const { return totalNum_; }

    private:
        std::vector<int> list_;
        int totalNum_;
    };

    // Java's `Object data` accepts either a Tuple or a List<Tuple>.
    using Data = std::variant<Tuple, std::vector<Tuple>>;

    static double mrr(const Data& data) {
        if (const Tuple* tuple = std::get_if<Tuple>(&data)) {
            const std::vector<int>& subList = tuple->getList();
            const int totalNum = tuple->getTotalNum();

            if (totalNum == 0) {
                return 0.0;
            }

            double mr = 0.0;
            for (std::size_t i = 0; i < subList.size(); ++i) {
                if (subList[i] == 1) {
                    mr = 1.0 / (i + 1);
                    break;
                }
            }
            return mr;
        } else if (const std::vector<Tuple>* tupleList =
                       std::get_if<std::vector<Tuple>>(&data)) {
            std::vector<double> separateResult;

            for (const Tuple& tuple : *tupleList) {
                const std::vector<int>& subList = tuple.getList();
                const int totalNum = tuple.getTotalNum();

                if (totalNum == 0) {
                    separateResult.push_back(0.0);
                } else {
                    double mr = 0.0;
                    for (std::size_t i = 0; i < subList.size(); ++i) {
                        if (subList[i] == 1) {
                            mr = 1.0 / (i + 1);
                            break;
                        }
                    }
                    separateResult.push_back(mr);
                }
            }
            return average(separateResult);
        }
        throw std::invalid_argument(
            "the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple");
    }

    static double map(const Data& data) {
        if (const Tuple* tuple = std::get_if<Tuple>(&data)) {
            const std::vector<int>& subList = tuple->getList();
            const int totalNum = tuple->getTotalNum();

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
        } else if (const std::vector<Tuple>* tupleList =
                       std::get_if<std::vector<Tuple>>(&data)) {
            std::vector<double> separateResult;

            for (const Tuple& tuple : *tupleList) {
                const std::vector<int>& subList = tuple.getList();
                const int totalNum = tuple.getTotalNum();

                if (totalNum == 0) {
                    separateResult.push_back(0.0);
                } else {
                    double ap = 0.0;
                    int count = 0;
                    for (std::size_t i = 0; i < subList.size(); ++i) {
                        if (subList[i] == 1) {
                            ++count;
                            ap += count / (i + 1.0);
                        }
                    }
                    separateResult.push_back(ap / totalNum);
                }
            }
            return average(separateResult);
        }
        throw std::invalid_argument(
            "the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple");
    }

private:
    // Equivalent of stream().mapToDouble(...).average().orElse(0.0):
    // sequential summation divided by count; 0.0 for empty input.
    static double average(const std::vector<double>& values) {
        if (values.empty()) {
            return 0.0;
        }
        double sum = 0.0;
        for (const double value : values) {
            sum += value;
        }
        return sum / static_cast<double>(values.size());
    }
};

}  // namespace org::example