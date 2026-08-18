#include <string>
#include <vector>
#include <limits>
#include <stdexcept>
#include <cstddef>
#include <utility>

class CombinationCalculator {
public:
    std::vector<std::string> datas;

    explicit CombinationCalculator(std::vector<std::string> datas)
        : datas(std::move(datas)) {}

    // Calculate the number of combinations for a specific count.
    static unsigned long long count(int n, int m) {
        if (m == 0 || n == m) {
            return 1;
        }
        return factorial(n) / (factorial(n - m) * factorial(m));
    }

    // Calculate the number of all possible combinations (2^n - 1).
    // Returns 0 (Python False) for n < 0 or n > 63, and +inf for n == 63.
    static double count_all(int n) {
        if (n < 0 || n > 63) {
            return 0;
        }
        if (n == 63) {
            return std::numeric_limits<double>::infinity();
        }
        return static_cast<double>((1ULL << n) - 1);
    }

    // Generate combinations with a specified number of elements.
    std::vector<std::vector<std::string>> select(int m) const {
        std::vector<std::vector<std::string>> result;
        // Mirrors [None] * m: negative m yields an empty list instead of an error.
        std::vector<std::string> resultList(m > 0 ? static_cast<std::size_t>(m) : 0);
        _select(0, resultList, 0, result);
        return result;
    }

    // Generate all possible combinations of selecting elements, using select().
    std::vector<std::vector<std::string>> select_all() const {
        std::vector<std::vector<std::string>> result;
        for (std::size_t i = 1; i <= datas.size(); ++i) {
            std::vector<std::vector<std::string>> selected = select(static_cast<int>(i));
            result.insert(result.end(), selected.begin(), selected.end());
        }
        return result;
    }

    // Generate combinations with a specified number of elements by recursion.
    void _select(int dataIndex, std::vector<std::string>& resultList, int resultIndex,
                 std::vector<std::vector<std::string>>& result) const {
        int resultLen = static_cast<int>(resultList.size());
        int resultCount = resultIndex + 1;
        if (resultCount > resultLen) {
            result.push_back(resultList);  // copy of the current combination
            return;
        }

        // Equivalent of range(dataIndex, len(datas) + resultCount - resultLen);
        // computed in signed arithmetic so a negative bound yields an empty loop.
        int loopEnd = static_cast<int>(datas.size()) + resultCount - resultLen;
        for (int i = dataIndex; i < loopEnd; ++i) {
            resultList[resultIndex] = datas[static_cast<std::size_t>(i)];
            _select(i + 1, resultList, resultIndex + 1, result);
        }
    }

private:
    static unsigned long long factorial(int n) {
        if (n < 0) {
            // Mirrors math.factorial raising ValueError for negative inputs.
            throw std::invalid_argument("factorial() not defined for negative values");
        }
        unsigned long long res = 1;
        for (int i = 2; i <= n; ++i) {
            res *= static_cast<unsigned long long>(i);
        }
        return res;
    }
};