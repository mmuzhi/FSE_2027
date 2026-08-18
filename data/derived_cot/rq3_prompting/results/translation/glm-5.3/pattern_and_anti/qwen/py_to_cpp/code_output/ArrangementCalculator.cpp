#include <vector>

class ArrangementCalculator {
public:
    std::vector<int> datas;

    ArrangementCalculator(std::vector<int> datas) : datas(std::move(datas)) {}

    // Equivalent of count(n) with m=None (or n == m): factorial(n)
    static long long count(int n) {
        return factorial(n);
    }

    static long long count(int n, int m) {
        if (n == m) {
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

    // Equivalent of select() with m=None: select all items
    std::vector<std::vector<int>> select() const {
        return select(static_cast<int>(datas.size()));
    }

    std::vector<std::vector<int>> select(int m) const {
        std::vector<std::vector<int>> result;
        std::vector<char> used(datas.size(), 0);
        std::vector<int> current;
        permute(m, used, current, result);
        return result;
    }

    std::vector<std::vector<int>> select_all() const {
        std::vector<std::vector<int>> result;
        for (int i = 1; i <= static_cast<int>(datas.size()); ++i) {
            std::vector<std::vector<int>> part = select(i);
            result.insert(result.end(), part.begin(), part.end());
        }
        return result;
    }

    static long long factorial(int n) {
        long long result = 1;
        for (int i = 2; i <= n; ++i) {
            result *= i;
        }
        return result;
    }

private:
    // Backtracking in ascending index order reproduces itertools.permutations
    // ordering (lexicographic over positions), including duplicate elements.
    void permute(int m, std::vector<char>& used, std::vector<int>& current,
                 std::vector<std::vector<int>>& out) const {
        if (static_cast<int>(current.size()) == m) {
            out.push_back(current);
            return;
        }
        for (int i = 0; i < static_cast<int>(datas.size()); ++i) {
            if (!used[i]) {
                used[i] = 1;
                current.push_back(datas[i]);
                permute(m, used, current, out);
                current.pop_back();
                used[i] = 0;
            }
        }
    }
};