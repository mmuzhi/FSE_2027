#include <vector>
#include <optional>
#include <cstddef>

template <typename T>
class ArrangementCalculator {
public:
    std::vector<T> datas;

    explicit ArrangementCalculator(std::vector<T> datas) : datas(std::move(datas)) {}

    static long long count(int n, std::optional<int> m = std::nullopt) {
        if (!m.has_value() || n == m.value()) {
            return factorial(n);
        } else {
            return factorial(n) / factorial(n - m.value());
        }
    }

    static long long count_all(int n) {
        long long total = 0;
        for (int i = 1; i <= n; ++i) {
            total += count(n, i);
        }
        return total;
    }

    std::vector<std::vector<T>> select(std::optional<int> m = std::nullopt) const {
        if (!m.has_value()) {
            m = static_cast<int>(datas.size());
        }
        std::vector<std::vector<T>> result;
        std::vector<int> current;
        std::vector<bool> used(datas.size(), false);
        permuteHelper(m.value(), current, used, result);
        return result;
    }

    std::vector<std::vector<T>> select_all() const {
        std::vector<std::vector<T>> result;
        for (int i = 1; i <= static_cast<int>(datas.size()); ++i) {
            std::vector<std::vector<T>> part = select(i);
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
    // Index-based recursion: matches itertools.permutations ordering exactly,
    // including duplicate-value elements (unlike std::next_permutation).
    void permuteHelper(int m, std::vector<int>& current, std::vector<bool>& used,
                       std::vector<std::vector<T>>& result) const {
        if (static_cast<int>(current.size()) == m) {
            std::vector<T> permutation;
            permutation.reserve(current.size());
            for (int idx : current) {
                permutation.push_back(datas[idx]);
            }
            result.push_back(std::move(permutation));
            return;
        }
        for (std::size_t i = 0; i < datas.size(); ++i) {
            if (!used[i]) {
                used[i] = true;
                current.push_back(static_cast<int>(i));
                permuteHelper(m, current, used, result);
                current.pop_back();
                used[i] = false;
            }
        }
    }
};