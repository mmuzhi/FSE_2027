#include <vector>
#include <string>
#include <cmath>
#include <cstdint>
#include <climits>

class CombinationCalculator {
public:
    CombinationCalculator(const std::vector<std::string>& datas) : datas(datas) {}

    static int count(int n, int m) {
        if (m == 0 || n == m) return 1;
        // Use a loop to avoid overflow? But Python uses factorial; we'll replicate using long long.
        long long result = 1;
        if (m > n - m) m = n - m;
        for (int i = 1; i <= m; ++i) {
            result = result * (n - m + i) / i;
        }
        return static_cast<int>(result);
    }

    // Note: Returns double to mimic Python's ability to return bool, int, or inf.
    // The original returns False for invalid, int for normal, and float('inf') for n==63.
    static double count_all(int n) {
        if (n < 0 || n > 63) return false; // false converted to double 0.0? But original returns bool False.
        // However, since return type is double, returning 0.0 differs from bool False.
        // To preserve exact behavior, we might need a variant. But for simplicity, we'll use double and treat false as 0.0.
        // Actually original returns False (boolean) for invalid. That's tricky. We'll keep double and just return 0.0 for invalid,
        // but note that Python would return False, not 0.0. For consistency, we could use a union or an optional.
        // To simplify and match intended use (int expected), we'll assume valid inputs.
        // But the spec says keep identical behavior. The stub says returns int, but implementation returns different types.
        // Since C++ is typed, we'll use double and return 0.0 for invalid. Alternatively, we could throw exception.
        // Given the instruction, I'll implement as per original: for n==63 return INFINITY, else return (1<<n)-1.
        if (n == 63) return INFINITY;
        return (1LL << n) - 1;
    }

    std::vector<std::vector<std::string>> select(int m) {
        std::vector<std::vector<std::string>> result;
        std::vector<std::string> resultList(m);
        _select(0, resultList, 0, result);
        return result;
    }

    std::vector<std::vector<std::string>> select_all() {
        std::vector<std::vector<std::string>> result;
        for (int i = 1; i <= static_cast<int>(datas.size()); ++i) {
            auto combos = select(i);
            result.insert(result.end(), combos.begin(), combos.end());
        }
        return result;
    }

private:
    std::vector<std::string> datas;

    void _select(int dataIndex, std::vector<std::string>& resultList, int resultIndex, std::vector<std::vector<std::string>>& result) {
        int resultLen = static_cast<int>(resultList.size());
        int resultCount = resultIndex + 1;
        if (resultCount > resultLen) {
            result.push_back(resultList);
            return;
        }
        int n = static_cast<int>(datas.size());
        for (int i = dataIndex; i < n + resultCount - resultLen; ++i) {
            resultList[resultIndex] = datas[i];
            _select(i + 1, resultList, resultIndex + 1, result);
        }
    }
};