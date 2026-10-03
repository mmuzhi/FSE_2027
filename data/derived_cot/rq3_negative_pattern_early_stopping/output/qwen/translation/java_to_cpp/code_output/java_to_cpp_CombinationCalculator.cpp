#include <vector>
#include <string>
#include <limits>

class CombinationCalculator {
private:
    std::vector<std::string> datas;

    static int factorial(int x) {
        int result = 1;
        for (int i = 1; i <= x; i++) {
            result *= i;
        }
        return result;
    }

    void _select(int dataIndex, std::vector<std::string>& resultList, int resultIndex, std::vector<std::vector<std::string>>& result, int m) {
        if (resultIndex == m) {
            result.push_back(resultList);
            return;
        }

        for (int i = dataIndex; i <= datas.size() - (m - resultIndex); i++) {
            resultList.insert(resultList.begin() + resultIndex, datas[i]);
            _select(i + 1, resultList, resultIndex + 1, result, m);
            resultList.erase(resultList.begin() + resultIndex);
        }
    }

public:
    CombinationCalculator(std::vector<std::string> datas) : datas(datas) {}

    static int count(int n, int m) {
        if (m == 0 || n == m) {
            return 1;
        }
        return factorial(n) / (factorial(n - m) * factorial(m));
    }

    static double countAll(int n) {
        if (n < 0 || n > 63) {
            return std::numeric_limits<double>::quiet_NaN();
        }
        if (n == 63) {
            return std::numeric_limits<double>::infinity();
        }
        return (1LL << n) - 1;
    }

    std::vector<std::vector<std::string>> select(int m) {
        std::vector<std::vector<std::string>> result;
        std::vector<std::string> resultList;
        _select(0, resultList, 0, result, m);
        return result;
    }

    std::vector<std::vector<std::string>> selectAll() {
        std::vector<std::vector<std::string>> result;
        for (int i = 1; i <= datas.size(); i++) {
            result.insert(result.end(), select(i).begin(), select(i).end());
        }
        return result;
    }
};