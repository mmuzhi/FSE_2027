#include <variant>
#include <vector>
#include <stdexcept>
#include <numeric>

class MetricsCalculator2 {
public:
    // Tuple class equivalent to the Java inner class
    struct Tuple {
        std::vector<int> list;
        int totalNum;

        Tuple(std::vector<int> list, int totalNum)
            : list(std::move(list)), totalNum(totalNum) {}

        const std::vector<int>& getList() const { return list; }
        int getTotalNum() const { return totalNum; }
    };

    // MRR metric
    static double mrr(const std::variant<Tuple, std::vector<Tuple>>& data) {
        // Check if data is a single Tuple
        if (std::holds_alternative<Tuple>(data)) {
            const Tuple& tuple = std::get<Tuple>(data);
            const std::vector<int>& subList = tuple.getList();
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
        }
        // Otherwise it must be a vector of Tuples (checked by variant)
        else {
            const std::vector<Tuple>& tupleList = std::get<std::vector<Tuple>>(data);
            std::vector<double> separateResult;

            for (const Tuple& tuple : tupleList) {
                const std::vector<int>& subList = tuple.getList();
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

            // Compute average, return 0.0 if empty
            if (separateResult.empty()) {
                return 0.0;
            }
            double sum = std::accumulate(separateResult.begin(), separateResult.end(), 0.0);
            return sum / separateResult.size();
        }
    }

    // MAP metric
    static double map(const std::variant<Tuple, std::vector<Tuple>>& data) {
        // Check if data is a single Tuple
        if (std::holds_alternative<Tuple>(data)) {
            const Tuple& tuple = std::get<Tuple>(data);
            const std::vector<int>& subList = tuple.getList();
            int totalNum = tuple.getTotalNum();

            if (totalNum == 0) {
                return 0.0;
            }

            double ap = 0.0;
            int count = 0;
            for (size_t i = 0; i < subList.size(); ++i) {
                if (subList[i] == 1) {
                    count++;
                    ap += count / static_cast<double>(i + 1);
                }
            }
            return ap / totalNum;
        }
        // Otherwise it must be a vector of Tuples
        else {
            const std::vector<Tuple>& tupleList = std::get<std::vector<Tuple>>(data);
            std::vector<double> separateResult;

            for (const Tuple& tuple : tupleList) {
                const std::vector<int>& subList = tuple.getList();
                int totalNum = tuple.getTotalNum();

                if (totalNum == 0) {
                    separateResult.push_back(0.0);
                } else {
                    double ap = 0.0;
                    int count = 0;
                    for (size_t i = 0; i < subList.size(); ++i) {
                        if (subList[i] == 1) {
                            count++;
                            ap += count / static_cast<double>(i + 1);
                        }
                    }
                    separateResult.push_back(ap / totalNum);
                }
            }

            // Compute average, return 0.0 if empty
            if (separateResult.empty()) {
                return 0.0;
            }
            double sum = std::accumulate(separateResult.begin(), separateResult.end(), 0.0);
            return sum / separateResult.size();
        }
    }
};