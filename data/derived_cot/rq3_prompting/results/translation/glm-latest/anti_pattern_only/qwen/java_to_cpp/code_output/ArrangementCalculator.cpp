#include <any>
#include <cstddef>
#include <iterator>
#include <optional>
#include <utility>
#include <vector>

namespace org {
namespace example {

class ArrangementCalculator {
public:
    explicit ArrangementCalculator(std::vector<std::any> datas)
        : datas(std::move(datas)) {}

    static int count(int n, std::optional<int> m) {
        if (!m.has_value() || n == m.value()) {
            return factorial(n);
        } else {
            return factorial(n) / factorial(n - m.value());
        }
    }

    static int countAll(int n) {
        int total = 0;
        for (int i = 1; i <= n; i++) {
            total += count(n, i);
        }
        return total;
    }

    std::vector<std::vector<std::any>> select(std::optional<int> m) const {
        if (!m.has_value()) {
            m = static_cast<int>(datas.size());
        }
        std::vector<std::vector<std::any>> result;
        selectPermutations(std::vector<std::any>{}, datas, m.value(), result);
        return result;
    }

    std::vector<std::vector<std::any>> selectAll() const {
        std::vector<std::vector<std::any>> result;
        for (int i = 1; i <= static_cast<int>(datas.size()); i++) {
            std::vector<std::vector<std::any>> selected = select(i);
            result.insert(result.end(),
                          std::make_move_iterator(selected.begin()),
                          std::make_move_iterator(selected.end()));
        }
        return result;
    }

    static int factorial(int n) {
        int result = 1;
        for (int i = 2; i <= n; i++) {
            result *= i;
        }
        return result;
    }

private:
    std::vector<std::any> datas;

    static void selectPermutations(const std::vector<std::any>& prefix,
                                   const std::vector<std::any>& remaining,
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
};

} // namespace example
} // namespace org