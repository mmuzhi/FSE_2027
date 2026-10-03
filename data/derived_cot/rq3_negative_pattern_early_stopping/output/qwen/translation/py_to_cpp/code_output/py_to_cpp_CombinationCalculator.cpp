#include <vector>
#include <string>
#include <variant>
#include <cmath>
#include <iostream>
#include <limits>

class CombinationCalculator {
private:
    std::vector<std::string> datas;

    // Helper function to compute factorial
    static long long factorial(int n) {
        if (n == 0 || n == 1) {
            return 1;
        }
        long long result = 1;
        for (int i = 2; i <= n; ++i) {
            result *= i;
        }
        return result;
    }

    // Helper function for recursive combination generation
    void _select(int dataIndex, std::vector<std::string>& resultList, int resultIndex, std::vector<std::vector<std::string>>& result) {
        int resultLen = resultList.size();
        int resultCount = resultIndex + 1;
        if (resultCount > resultLen) {
            result.push_back(resultList);
            return;
        }

        for (int i = dataIndex; i < datas.size() + (resultLen - resultCount); ++i) {
            resultList[resultIndex] = datas[i];
            _select(i + 1, resultList, resultIndex + 1, result);
        }
    }

public:
    CombinationCalculator(const std::vector<std::string>& datas) : datas(datas) {}

    // Calculate the number of combinations for specific count
    static long long count(int n, int m) {
        if (m == 0 || n == m) {
            return 1;
        }
        return factorial(n) / (factorial(n - m) * factorial(m));
    }

    // Calculate the number of all possible combinations
    static std::variant<long long, double, bool> count_all(int n) {
        if (n < 0 || n > 63) {
            return false;
        }
        if (n == 63) {
            return std::numeric_limits<double>::infinity();
        }
        return (1LL << n) - 1;
    }

    // Generate combinations with a specified number of elements
    std::vector<std::vector<std::string>> select(int m) {
        std::vector<std::vector<std::string>> result;
        std::vector<std::string> resultList(m, "");
        _select(0, resultList, 0, result);
        return result;
    }

    // Generate all possible combinations
    std::vector<std::vector<std::string>> select_all() {
        std::vector<std::vector<std::string>> result;
        for (int i = 1; i <= datas.size(); ++i) {
            result.insert(result.end(), select(i).begin(), select(i).end());
        }
        return result;
    }
};