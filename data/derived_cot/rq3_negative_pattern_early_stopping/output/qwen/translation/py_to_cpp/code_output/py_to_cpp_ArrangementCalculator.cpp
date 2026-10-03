#include <vector>
#include <algorithm>

template <typename T>
class ArrangementCalculator {
private:
    std::vector<T> datas;

    // Helper function to generate combinations of indices
    static void generate_combinations(int n, int m, int start, std::vector<int>& current, std::vector<std::vector<int>>& result) {
        if (current.size() == m) {
            result.push_back(current);
            return;
        }
        for (int i = start; i < n; i++) {
            current.push_back(i);
            generate_combinations(n, m, i+1, current, result);
            current.pop_back();
        }
    }

    // Helper function to generate permutations for a given m from the data
    static std::vector<std::vector<T>> generate_permutations(const std::vector<T>& data, int m) {
        if (m > static_cast<int>(data.size()) || m < 0) {
            return {};
        }
        std::vector<bool> chosen(data.size(), false);
        std::vector<int> current;
        std::vector<std::vector<int>> all_combinations;

        // Generate all combinations of indices of size m from data.size()
        std::vector<int> comb;
        generate_combinations(data.size(), m, 0, comb, all_combinations);

        std::vector<std::vector<T>> result;
        for (const auto& comb : all_combinations) {
            // Generate all permutations of this combination
            std::vector<int> perm = comb;
            std::sort(perm.begin(), perm.end());
            do {
                std::vector<T> arr;
                for (int idx : perm) {
                    arr.push_back(data[idx]);
                }
                result.push_back(arr);
            } while (std::next_permutation(perm.begin(), perm.end()));
        }
        return result;
    }

public:
    ArrangementCalculator(const std::vector<T>& datas) : datas(datas) {}

    // Count the number of arrangements (permutations) of n taken m at a time, or n! if m is None or n==m.
    static long count(int n, int m = -1) {
        if (m == -1 || n == m) {
            return factorial(n);
        } else {
            return factorial(n) / factorial(n - m);
        }
    }

    // Count the total number of arrangements for all lengths from 1 to n.
    static long count_all(int n) {
        long total = 0;
        for (int i = 1; i <= n; i++) {
            total += count(n, i);
        }
        return total;
    }

    // Generate a list of arrangements by selecting m items from the internal datas.
    std::vector<std::vector<T>> select(int m = -1) {
        if (m == -1) {
            m = datas.size();
        }
        if (m > static_cast<int>(datas.size()) || m < 0) {
            return {};
        }
        return generate_permutations(datas, m);
    }

    // Generate a list of all arrangements by selecting at least 1 item and at most the number of internal datas.
    std::vector<std::vector<T>> select_all() {
        std::vector<std::vector<T>> result;
        int n = datas.size();
        for (int i = 1; i <= n; i++) {
            result.insert(result.end(), select(i));
        }
        return result;
    }

    // Calculate the factorial of a given number.
    static long factorial(int n) {
        if (n < 0) {
            // In the original Python code, factorial(-1) returns 1 because the loop doesn't run.
            long result = 1;
            for (int i = 2; i <= n; i++) {
                result *= i;
            }
            return result;
        }
        long result = 1;
        for (int i = 2; i <= n; i++) {
            result *= i;
        }
        return result;
    }
};