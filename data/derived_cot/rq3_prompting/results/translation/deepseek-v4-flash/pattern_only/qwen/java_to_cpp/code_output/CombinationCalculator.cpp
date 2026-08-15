#include <vector>
#include <string>
#include <cstdint>
#include <limits>
#include <stdexcept>

class CombinationCalculator {
private:
    std::vector<std::string> datas;

    static int32_t multiply(int32_t a, int32_t b) {
        return static_cast<int32_t>(static_cast<uint32_t>(a) * static_cast<uint32_t>(b));
    }

    static int32_t divide(int32_t a, int32_t b) {
        if (b == 0) {
            throw std::runtime_error("/ by zero");
        }
        if (b == -1 && a == std::numeric_limits<int32_t>::min()) {
            return a;
        }
        return a / b;
    }

    static int32_t factorial(int32_t x) {
        int32_t result = 1;
        for (int32_t i = 1; i <= x; i = static_cast<int32_t>(static_cast<uint32_t>(i) + 1)) {
            result = multiply(result, i);
        }
        return result;
    }

public:
    CombinationCalculator(const std::vector<std::string>& datas) : datas(datas) {}

    static int count(int n, int m) {
        if (m == 0 || n == m) {
            return 1;
        }
        return divide(factorial(n), multiply(factorial(n - m), factorial(m)));
    }

    static double countAll(int n) {
        if (n < 0 || n > 63) {
            return std::numeric_limits<double>::quiet_NaN();
        }
        if (n == 63) {
            return std::numeric_limits<double>::infinity();
        }
        uint32_t u = (static_cast<uint32_t>(1) << (n & 31)) - 1;
        return static_cast<double>(static_cast<int32_t>(u));
    }

    std::vector<std::vector<std::string>> select(int m) {
        if (m < 0) {
            throw std::invalid_argument("Illegal Capacity: " + std::to_string(m));
        }
        std::vector<std::vector<std::string>> result;
        std::vector<std::string> resultList;
        resultList.reserve(m);
        _select(0, resultList, 0, result, m);
        return result;
    }

    std::vector<std::vector<std::string>> selectAll() {
        std::vector<std::vector<std::string>> result;
        int n = static_cast<int>(datas.size());
        for (int i = 1; i <= n; i = static_cast<int>(static_cast<uint32_t>(i) + 1)) {
            std::vector<std::vector<std::string>> selected = select(i);
            result.insert(result.end(), selected.begin(), selected.end());
        }
        return result;
    }

protected:
    void _select(int dataIndex, std::vector<std::string>& resultList, int resultIndex,
                 std::vector<std::vector<std::string>>& result, int m) {
        if (resultIndex == m) {
            result.push_back(resultList);
            return;
        }
        for (int i = dataIndex; i <= static_cast<int>(datas.size()) - (m - resultIndex);
             i = static_cast<int>(static_cast<uint32_t>(i) + 1)) {
            resultList.insert(resultList.begin() + resultIndex, datas.at(i));
            _select(static_cast<int>(static_cast<uint32_t>(i) + 1), resultList, resultIndex + 1, result, m);
            resultList.erase(resultList.begin() + resultIndex);
        }
    }
};