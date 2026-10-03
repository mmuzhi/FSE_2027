#include <vector>
#include <string>
#include <cmath>

class CombinationCalculator {
public:
    CombinationCalculator(const std::vector<std::string>& datas) : datas(datas) {}

    static int count(int n, int m) {
        if (m == 0 || n == m) return 1;
        return factorial(n) / (factorial(n - m) * factorial(m));
    }

    static double countAll(int n) {
        if (n < 0 || n > 63) return std::numeric_limits<double>::quiet_NaN();
        if (n == 63) return std::numeric_limits<double>::infinity();
        int shiftAmt = n & 0x1F;
        unsigned int u = (1u << shiftAmt) - 1u;
        return static_cast<double>(static_cast<int>(u));
    }

    std::vector<std::vector<std::string>> select(int m) const {
        std::vector<std::vector<std::string>> result;
        std::vector<std::string> current(m);
        _select(0, current, 0, result, m);
        return result;
    }

    std::vector<std::vector<std::string>> selectAll() const {
        std::vector<std::vector<std::string>> result;
        for (int i = 1; i <= static_cast<int>(datas.size()); ++i) {
            auto combos = select(i);
            result.insert(result.end(), combos.begin(), combos.end());
        }
        return result;
    }

private:
    static int factorial(int x) {
        int result = 1;
        for (int i = 1; i <= x; ++i) result *= i;
        return result;
    }

    void _select(int dataIndex, std::vector<std::string>& current, int resultIndex,
                 std::vector<std::vector<std::string>>& result, int m) const {
        if (resultIndex == m) {
            result.push_back(current);
            return;
        }
        for (int i = dataIndex; i <= static_cast<int>(datas.size()) - (m - resultIndex); ++i) {
            current[resultIndex] = datas[i];
            _select(i + 1, current, resultIndex + 1, result, m);
        }
    }

    std::vector<std::string> datas;
};