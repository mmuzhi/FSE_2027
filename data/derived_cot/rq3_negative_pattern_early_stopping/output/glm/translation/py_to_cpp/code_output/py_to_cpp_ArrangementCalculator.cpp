#include <vector>
#include <utility>

template <typename T>
class ArrangementCalculator {
public:
    std::vector<T> datas;

    ArrangementCalculator(std::vector<T> datas) : datas(std::move(datas)) {}

    static long long count(int n, int m) {
        if (n == m) {
            return factorial(n);
        } else {
            return factorial(n) / factorial(n - m);
        }
    }

    static long long count(int n) {
        return factorial(n);
    }

    static long long count_all(int n) {
        long long total = 0;
        for (int i = 1; i <= n; ++i) {
            total += count(n, i);
        }
        return total;
    }

    std::vector<std::vector<T>> select(int m) {
        std::vector<std::vector<T>> result;
        std::vector<T> current;
        std::vector<bool> used(datas.size(), false);
        generate_permutations(datas, m, 0, current, used, result);
        return result;
    }

    std::vector<std::vector<T>> select() {
        return select(static_cast<int>(datas.size()));
    }

    std::vector<std::vector<T>> select_all() {
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
    static void generate_permutations(const std::vector<T>& datas, int m, int index, std::vector<T>& current, std::vector<bool>& used, std::vector<std::vector<T>>& result) {
        if (index == m) {
            result.push_back(current);
            return;
        }
        for (size_t i = 0; i < datas.size(); ++i) {
            if (!used[i]) {
                used[i] = true;
                current.push_back(datas[i]);
                generate_permutations(datas, m, index + 1, current, used, result);
                current.pop_back();
                used[i] = false;
            }
        }
    }
};