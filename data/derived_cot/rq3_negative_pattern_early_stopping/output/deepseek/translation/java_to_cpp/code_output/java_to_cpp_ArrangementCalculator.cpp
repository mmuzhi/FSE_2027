#include <vector>
#include <any>
#include <optional>

class ArrangementCalculator {
private:
    std::vector<std::any> datas;

    // Recursive helper to generate permutations
    void selectPermutations(std::vector<std::any> prefix,
                            std::vector<std::any> remaining,
                            int m,
                            std::vector<std::vector<std::any>>& result) {
        if (static_cast<int>(prefix.size()) == m) {
            result.push_back(prefix);
            return;
        }
        for (size_t i = 0; i < remaining.size(); ++i) {
            std::vector<std::any> newPrefix = prefix;
            newPrefix.push_back(remaining[i]);
            std::vector<std::any> newRemaining = remaining;
            newRemaining.erase(newRemaining.begin() + static_cast<long>(i));
            selectPermutations(newPrefix, newRemaining, m, result);
        }
    }

public:
    ArrangementCalculator(const std::vector<std::any>& datas)
        : datas(datas) {}

    // Count arrangements of n items taken m at a time.
    // If m is not given (null), it defaults to n (full permutations).
    static int count(int n, std::optional<int> m = std::nullopt) {
        if (!m.has_value() || n == m.value()) {
            return factorial(n);
        } else {
            return factorial(n) / factorial(n - m.value());
        }
    }

    // Count all arrangements of n items (i from 1 to n)
    static int countAll(int n) {
        int total = 0;
        for (int i = 1; i <= n; ++i) {
            total += count(n, i);
        }
        return total;
    }

    // Select arrangements of size m from the stored data.
    // If m is not given, it selects full permutations (m = datas.size()).
    std::vector<std::vector<std::any>> select(std::optional<int> m = std::nullopt) {
        if (!m.has_value()) {
            m = static_cast<int>(datas.size());
        }
        std::vector<std::vector<std::any>> result;
        selectPermutations({}, datas, m.value(), result);
        return result;
    }

    // Select all arrangements of all sizes (1 to datas.size()).
    std::vector<std::vector<std::any>> selectAll() {
        std::vector<std::vector<std::any>> result;
        for (int i = 1; i <= static_cast<int>(datas.size()); ++i) {
            auto part = select(i);
            result.insert(result.end(), part.begin(), part.end());
        }
        return result;
    }

    // Compute factorial of n (n >= 0)
    static int factorial(int n) {
        int result = 1;
        for (int i = 2; i <= n; ++i) {
            result *= i;
        }
        return result;
    }
};