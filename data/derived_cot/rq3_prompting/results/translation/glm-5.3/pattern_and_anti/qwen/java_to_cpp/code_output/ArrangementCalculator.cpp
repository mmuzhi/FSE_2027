#include <cstddef>
#include <optional>
#include <utility>
#include <vector>

template <typename T>
class ArrangementCalculator {
private:
    std::vector<T> datas;

public:
    explicit ArrangementCalculator(std::vector<T> datas) : datas(std::move(datas)) {}

    static int count(int n, std::optional<int> m) {
        if (!m.has_value() || n == *m) {
            return factorial(n);
        }
        else {
            return factorial(n) / factorial(n - *m);
        }
    }

    static int countAll(int n) {
        int total = 0;
        for (int i = 1; i <= n; i++) {
            total += count(n, i);
        }
        return total;
    }

    std::vector<std::vector<T>> select(std::optional<int> m) const {
        if (!m.has_value()) {
            m = static_cast<int>(datas.size());
        }
        std::vector<std::vector<T>> result;
        selectPermutations(std::vector<T>{}, datas, *m, result);
        return result;
    }

    std::vector<std::vector<T>> selectAll() const {
        std::vector<std::vector<T>> result;
        for (int i = 1; i <= static_cast<int>(datas.size()); i++) {
            std::vector<std::vector<T>> sub = select(i);
            result.insert(result.end(), sub.begin(), sub.end());
        }
        return result;
    }

    static int factorial(int n) {
        int result = 1;
        for (int i = 2; i <= n; i++) {
            // Unsigned arithmetic mirrors Java's wrap-around on int overflow.
            result = static_cast<int>(static_cast<unsigned int>(result) *
                                      static_cast<unsigned int>(i));
        }
        return result;
    }

private:
    void selectPermutations(std::vector<T> prefix, std::vector<T> remaining, int m,
                            std::vector<std::vector<T>>& result) const {
        if (static_cast<int>(prefix.size()) == m) {
            result.push_back(prefix);
            return;
        }
        for (std::size_t i = 0; i < remaining.size(); i++) {
            std::vector<T> newPrefix = prefix;
            newPrefix.push_back(remaining[i]);
            std::vector<T> newRemaining = remaining;
            newRemaining.erase(newRemaining.begin() + static_cast<std::ptrdiff_t>(i));
            selectPermutations(std::move(newPrefix), std::move(newRemaining), m, result);
        }
    }
};