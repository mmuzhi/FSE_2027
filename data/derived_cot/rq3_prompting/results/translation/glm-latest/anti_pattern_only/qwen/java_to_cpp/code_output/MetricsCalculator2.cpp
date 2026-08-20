#include <cstddef>
#include <stdexcept>
#include <utility>
#include <variant>
#include <vector>

namespace org::example {

class MetricsCalculator2 {
public:
    // Equivalent of the Java nested class MetricsCalculator2.Tuple.
    class Tuple {
    public:
        Tuple(std::vector<int> list, int totalNum)
            : list_(std::move(list)), totalNum_(totalNum) {}

        std::vector<int>& getList() { return list_; }
        const std::vector<int>& getList() const { return list_; }

        int getTotalNum() const { return totalNum_; }

    private:
        std::vector<int> list_;
        int totalNum_;
    };

    // Stand-in for the Java `Object` parameter: either a single Tuple, a list
    // of Tuples, or "something else" (std::monostate), which triggers the same
    // IllegalArgumentException as the Java instanceof checks.
    using Input = std::variant<std::monostate, Tuple, std::vector<Tuple>>;

    static double mrr(const Input& data) {
        if (!std::holds_alternative<Tuple>(data) &&
            !std::holds_alternative<std::vector<Tuple>>(data)) {
            throw std::invalid_argument(
                "the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple");
        }

        if (const Tuple* tuple = std::get_if<Tuple>(&data)) {
            const std::vector<int>& subList = tuple->getList();
            const int totalNum = tuple->getTotalNum();

            if (totalNum == 0) {
                return 0.0;
            }

            double mr = 0.0;
            for (std::size_t i = 0; i < subList.size(); i++) {
                if (subList[i] == 1) {
                    mr = 1.0 / (i + 1);
                    break;
                }
            }
            return mr;
        } else {
            const std::vector<Tuple>& tupleList = std::get<std::vector<Tuple>>(data);
            std::vector<double> separateResult;

            for (const Tuple& tuple : tupleList) {
                const std::vector<int>& subList = tuple.getList();
                const int totalNum = tuple.getTotalNum();

                if (totalNum == 0) {
                    separateResult.push_back(0.0);
                } else {
                    double mr = 0.0;
                    for (std::size_t i = 0; i < subList.size(); i++) {
                        if (subList[i] == 1) {
                            mr = 1.0 / (i + 1);
                            break;
                        }
                    }
                    separateResult.push_back(mr);
                }
            }
            return averageOrZero(separateResult);
        }
    }

    static double map(const Input& data) {
        if (!std::holds_alternative<Tuple>(data) &&
            !std::holds_alternative<std::vector<Tuple>>(data)) {
            throw std::invalid_argument(
                "the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple");
        }

        if (const Tuple* tuple = std::get_if<Tuple>(&data)) {
            const std::vector<int>& subList = tuple->getList();
            const int totalNum = tuple->getTotalNum();

            if (totalNum == 0) {
                return 0.0;
            }

            double ap = 0.0;
            int count = 0;
            for (std::size_t i = 0; i < subList.size(); i++) {
                if (subList[i] == 1) {
                    count++;
                    ap += count / (i + 1.0);
                }
            }
            return ap / totalNum;
        } else {
            const std::vector<Tuple>& tupleList = std::get<std::vector<Tuple>>(data);
            std::vector<double> separateResult;

            for (const Tuple& tuple : tupleList) {
                const std::vector<int>& subList = tuple.getList();
                const int totalNum = tuple.getTotalNum();

                if (totalNum == 0) {
                    separateResult.push_back(0.0);
                } else {
                    double ap = 0.0;
                    int count = 0;
                    for (std::size_t i = 0; i < subList.size(); i++) {
                        if (subList[i] == 1) {
                            count++;
                            ap += count / (i + 1.0);
                        }
                    }
                    separateResult.push_back(ap / totalNum);
                }
            }
            return averageOrZero(separateResult);
        }
    }

private:
    // Equivalent of Java's
    // separateResult.stream().mapToDouble(Double::doubleValue).average().orElse(0.0)
    // (sequential left-to-right summation, then division by the count;
    //  0.0 when the list is empty).
    static double averageOrZero(const std::vector<double>& values) {
        if (values.empty()) {
            return 0.0;
        }
        double sum = 0.0;
        for (double value : values) {
            sum += value;
        }
        return sum / static_cast<double>(values.size());
    }
};

}  // namespace org::example