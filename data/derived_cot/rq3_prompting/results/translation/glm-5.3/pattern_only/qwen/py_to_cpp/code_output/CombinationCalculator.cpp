#include <limits>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

class CombinationCalculator {
public:
    std::vector<std::string> datas;

    explicit CombinationCalculator(std::vector<std::string> datas)
        : datas(std::move(datas)) {}

    // Calculate the number of combinations for a specific count.
    static long long count(int n, int m) {
        if (m == 0 || n == m) {
            return 1;
        }
        unsigned long long num = factorial(n);
        // Mirrors Python: math.factorial(n) // (math.factorial(n - m) * math.factorial(m))
        // Negative arguments raise (like Python's ValueError).
        unsigned long long den = factorial(n - m) * factorial(m);
        return static_cast<long long>(num / den);
    }

    // Calculate the number of all possible combinations.
    // Returns 0 (Python's False) for out-of-range n, and infinity for n == 63.
    static double count_all(int n) {
        if (n < 0 || n > 63) {
            return 0;
        }
        if (n == 63) {
            return std::numeric_limits<double>::infinity();
        }
        return static_cast<double>((1ULL << n) - 1ULL);
    }

    // Generate combinations with a specified number of elements.
    std::vector<std::vector<std::string>> select(int m) const {
        std::vector<std::vector<std::string>> result;
        // Python's [None] * m yields an empty list for m <= 0.
        std::vector<std::string> resultList(static_cast<size_t>(m > 0 ? m : 0));
        _select(0, resultList, 0, result);
        return result;
    }

    // Generate all possible combinations of selecting elements from the data list.
    std::vector<std::vector<std::string>> select_all() const {
        std::vector<std::vector<std::string>> result;
        for (int i = 1; i <= static_cast<int>(datas.size()); ++i) {
            std::vector<std::vector<std::string>> combos = select(i);
            result.insert(result.end(), combos.begin(), combos.end());
        }
        return result;
    }

    // Generate combinations with a specified number of elements by recursion.
    void _select(int dataIndex, std::vector<std::string>& resultList, int resultIndex,
                 std::vector<std::vector<std::string>>& result) const {
        int resultLen = static_cast<int>(resultList.size());
        int resultCount = resultIndex + 1;
        if (resultCount > resultLen) {
            result.push_back(resultList); // copy, like Python's resultList.copy()
            return;
        }

        int end = static_cast<int>(datas.size()) + resultCount - resultLen;
        for (int i = dataIndex; i < end; ++i) {
            resultList[resultIndex] = datas[i];
            _select(i + 1, resultList, resultIndex + 1, result);
        }
    }

private:
    static unsigned long long factorial(int x) {
        if (x < 0) {
            // math.factorial raises ValueError for negative inputs.
            throw std::invalid_argument("factorial() not defined for negative values");
        }
        unsigned long long r = 1;
        for (int i = 2; i <= x; ++i) {
            r *= static_cast<unsigned long long>(i);
        }
        return r;
    }
};