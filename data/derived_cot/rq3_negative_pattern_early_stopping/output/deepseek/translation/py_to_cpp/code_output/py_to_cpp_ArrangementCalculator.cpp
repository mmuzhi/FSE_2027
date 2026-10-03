#include <vector>

class ArrangementCalculator {
private:
    std::vector<int> datas;

    static long long factorial(int n) {
        long long result = 1;
        for (int i = 2; i <= n; ++i) {
            result *= i;
        }
        return result;
    }

    std::vector<std::vector<int>> generatePermutations(int m) const {
        std::vector<std::vector<int>> result;
        std::vector<int> current;
        std::vector<bool> used(datas.size(), false);
        backtrack(current, used, m, result);
        return result;
    }

    void backtrack(std::vector<int>& current, std::vector<bool>& used, int m, std::vector<std::vector<int>>& result) const {
        if ((int)current.size() == m) {
            result.push_back(current);
            return;
        }
        for (int i = 0; i < (int)datas.size(); ++i) {
            if (!used[i]) {
                used[i] = true;
                current.push_back(datas[i]);
                backtrack(current, used, m, result);
                current.pop_back();
                used[i] = false;
            }
        }
    }

public:
    ArrangementCalculator(const std::vector<int>& datas) : datas(datas) {}

    static long long count(int n, int m = -1) {
        if (m == -1 || n == m) {
            return factorial(n);
        } else {
            return factorial(n) / factorial(n - m);
        }
    }

    static long long count_all(int n) {
        long long total = 0;
        for (int i = 1; i <= n; ++i) {
            total += count(n, i);
        }
        return total;
    }

    std::vector<std::vector<int>> select(int m = -1) {
        if (m == -1) {
            m = datas.size();
        }
        return generatePermutations(m);
    }

    std::vector<std::vector<int>> select_all() {
        std::vector<std::vector<int>> result;
        for (int i = 1; i <= (int)datas.size(); ++i) {
            auto perms = select(i);
            result.insert(result.end(), perms.begin(), perms.end());
        }
        return result;
    }
};