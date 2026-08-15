#include <vector>
#include <optional>
#include <stdexcept>
#include <utility>

class ArrangementCalculator {
public:
    ArrangementCalculator(std::vector<int> datas) : datas(std::move(datas)) {}

    static long long count(int n, std::optional<int> m = std::nullopt) {
        if (!m.has_value() || n == m.value()) {
            return factorial(n);
        }
        return factorial(n) / factorial(n - m.value());
    }

    static long long count_all(int n) {
        long long total = 0;
        for (int i = 1; i <= n; ++i) {
            total += count(n, i);
        }
        return total;
    }

    std::vector<std::vector<int>> select(std::optional<int> m = std::nullopt) {
        int r = m.has_value() ? m.value() : static_cast<int>(datas.size());
        if (r < 0) {
            throw std::invalid_argument("r must be non-negative");
        }

        std::vector<std::vector<int>> result;
        if (r > static_cast<int>(datas.size())) {
            return result;
        }

        std::vector<int> current;
        std::vector<bool> used(datas.size(), false);
        backtrack(current, used, r, result);
        return result;
    }

    std::vector<std::vector<int>> select_all() {
        std::vector<std::vector<int>> result;
        for (int i = 1; i <= static_cast<int>(datas.size()); ++i) {
            std::vector<std::vector<int>> selected = select(i);
            result.insert(result.end(), selected.begin(), selected.end());
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
    std::vector<int> datas;

    void backtrack(std::vector<int>& current, std::vector<bool>& used, int m,
                   std::vector<std::vector<int>>& result) {
        if (current.size() == static_cast<size_t>(m)) {
            result.push_back(current);
            return;
        }

        for (int i = 0; i < static_cast<int>(datas.size()); ++i) {
            if (!used[i]) {
                used[i] = true;
                current.push_back(datas[i]);
                backtrack(current, used, m, result);
                current.pop_back();
                used[i] = false;
            }
        }
    }
};