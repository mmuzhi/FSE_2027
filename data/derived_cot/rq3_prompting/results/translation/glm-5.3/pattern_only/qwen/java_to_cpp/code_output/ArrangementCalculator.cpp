#include <vector>
#include <optional>
#include <any>

namespace org {
namespace example {

class ArrangementCalculator {
private:
    std::vector<std::any> datas;

public:
    explicit ArrangementCalculator(std::vector<std::any> datas)
        : datas(std::move(datas)) {}

    static int count(int n, std::optional<int> m) {
        if (!m.has_value() || n == *m) {
            return factorial(n);
        } else {
            return factorial(n) / factorial(n - *m);
        }
    }

    static int countAll(int n) {
        // unsigned arithmetic preserves Java's int overflow wrap-around
        unsigned int total = 0;
        for (int i = 1; i <= n; i++) {
            total += static_cast<unsigned int>(count(n, i));
        }
        return static_cast<int>(total);
    }

    std::vector<std::vector<std::any>> select(std::optional<int> m) {
        if (!m.has_value()) {
            m = static_cast<int>(datas.size());
        }
        std::vector<std::vector<std::any>> result;
        selectPermutations(std::vector<std::any>{}, datas, *m, result);
        return result;
    }

    std::vector<std::vector<std::any>> selectAll() {
        std::vector<std::vector<std::any>> result;
        for (int i = 1; i <= static_cast<int>(datas.size()); i++) {
            std::vector<std::vector<std::any>> sub = select(i);
            result.insert(result.end(), sub.begin(), sub.end());
        }
        return result;
    }

private:
    void selectPermutations(std::vector<std::any> prefix,
                            std::vector<std::any> remaining,
                            int m,
                            std::vector<std::vector<std::any>>& result) {
        if (static_cast<int>(prefix.size()) == m) {
            result.push_back(prefix);
            return;
        }
        for (std::size_t i = 0; i < remaining.size(); i++) {
            std::vector<std::any> newPrefix = prefix;
            newPrefix.push_back(remaining[i]);
            std::vector<std::any> newRemaining = remaining;
            newRemaining.erase(newRemaining.begin() + static_cast<std::ptrdiff_t>(i));
            selectPermutations(std::move(newPrefix), std::move(newRemaining), m, result);
        }
    }

public:
    static int factorial(int n) {
        // unsigned arithmetic preserves Java's int overflow wrap-around
        unsigned int result = 1;
        for (int i = 2; i <= n; i++) {
            result *= static_cast<unsigned int>(i);
        }
        return static_cast<int>(result);
    }
};

} // namespace example
} // namespace org