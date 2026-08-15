#include <vector>
#include <string>
#include <stdexcept>
#include <variant>
#include <limits>
#include <algorithm>
#include <boost/multiprecision/cpp_int.hpp>

using boost::multiprecision::cpp_int;

class CombinationCalculator {
private:
    std::vector<std::string> datas;

    void _select(int dataIndex, std::vector<std::string>& resultList, int resultIndex,
                 std::vector<std::vector<std::string>>& result) {
        int resultLen = static_cast<int>(resultList.size());
        int resultCount = resultIndex + 1;
        if (resultCount > resultLen) {
            result.push_back(resultList);
            return;
        }
        int dataSize = static_cast<int>(datas.size());
        for (int i = dataIndex; i < dataSize + resultCount - resultLen; ++i) {
            resultList[resultIndex] = datas[i];
            _select(i + 1, resultList, resultIndex + 1, result);
        }
    }

public:
    CombinationCalculator(const std::vector<std::string>& datas) : datas(datas) {}

    static cpp_int count(int n, int m) {
        if (m == 0 || n == m) {
            return cpp_int(1);
        }
        if (n < 0 || m < 0 || m > n) {
            throw std::invalid_argument("math domain error");
        }
        m = std::min(m, n - m);
        cpp_int result = 1;
        for (int i = 1; i <= m; ++i) {
            result = result * (n - m + i) / i;
        }
        return result;
    }

    static std::variant<long long, double> count_all(int n) {
        if (n < 0) {
            throw std::invalid_argument("negative shift count");
        }
        if (n > 63) {
            return std::numeric_limits<double>::infinity();
        }
        return static_cast<long long>((1ULL << n) - 1);
    }

    std::vector<std::vector<std::string>> select(int m) {
        if (m <= 0) {
            return {{}};
        }
        std::vector<std::vector<std::string>> result;
        std::vector<std::string> resultList(m);
        _select(0, resultList, 0, result);
        return result;
    }

    std::vector<std::vector<std::string>> select_all() {
        std::vector<std::vector<std::string>> result;
        for (int i = 1; i <= static_cast<int>(datas.size()); ++i) {
            std::vector<std::vector<std::string>> combos = select(i);
            result.insert(result.end(), combos.begin(), combos.end());
        }
        return result;
    }
};