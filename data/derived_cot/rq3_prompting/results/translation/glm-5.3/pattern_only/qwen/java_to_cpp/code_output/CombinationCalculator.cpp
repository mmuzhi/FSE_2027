#include <limits>
#include <string>
#include <vector>

namespace org {
namespace example {

class CombinationCalculator {
private:
    // Java stores a reference to the caller's list; keep aliasing semantics.
    std::vector<std::string>& datas;

    static int factorial(int x) {
        // unsigned arithmetic emulates Java's wraparound on int overflow
        unsigned result = 1;
        for (int i = 1; i <= x; ++i) {
            result *= static_cast<unsigned>(i);
        }
        return static_cast<int>(result);
    }

public:
    CombinationCalculator(std::vector<std::string>& datas_) : datas(datas_) {}

    static int count(int n, int m) {
        if (m == 0 || n == m) {
            return 1;
        }
        int num = factorial(n);
        int prod = static_cast<int>(static_cast<unsigned>(factorial(n - m)) *
                                    static_cast<unsigned>(factorial(m)));
        return num / prod;  // truncation toward zero, same as Java
    }

    static double countAll(int n) {
        if (n < 0 || n > 63) {
            return std::numeric_limits<double>::quiet_NaN();
        }
        if (n == 63) {
            return std::numeric_limits<double>::infinity();
        }
        // Java: (1 << n) - 1 on int — shift distance masked to n & 31,
        // arithmetic wraps; replicate exactly (avoids UB in C++).
        return static_cast<double>(static_cast<int>((1u << (n & 31)) - 1u));
    }

    std::vector<std::vector<std::string>> select(int m) {
        std::vector<std::vector<std::string>> result;
        std::vector<std::string> resultList;
        _select(0, resultList, 0, result, m);
        return result;
    }

    std::vector<std::vector<std::string>> selectAll() {
        std::vector<std::vector<std::string>> result;
        for (int i = 1; i <= static_cast<int>(datas.size()); ++i) {
            std::vector<std::vector<std::string>> sub = select(i);
            result.insert(result.end(), sub.begin(), sub.end());
        }
        return result;
    }

protected:
    void _select(int dataIndex, std::vector<std::string>& resultList, int resultIndex,
                 std::vector<std::vector<std::string>>& result, int m) {
        if (resultIndex == m) {
            result.push_back(resultList);  // copy, like new ArrayList<>(resultList)
            return;
        }

        for (int i = dataIndex; i <= static_cast<int>(datas.size()) - (m - resultIndex); ++i) {
            resultList.insert(resultList.begin() + resultIndex, datas[i]);
            _select(i + 1, resultList, resultIndex + 1, result, m);
            resultList.erase(resultList.begin() + resultIndex);
        }
    }
};

} // namespace example
} // namespace org