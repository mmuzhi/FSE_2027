#include <vector>
#include <memory>
#include <optional>
#include <stdexcept>

class ArrangementCalculator {
public:
    using Object = std::shared_ptr<void>;
    using List = std::vector<Object>;

private:
    List* datas;

public:
    ArrangementCalculator(List* datas) : datas(datas) {}
    ArrangementCalculator(List& datas) : datas(&datas) {}

    static int count(int n, std::optional<int> m) {
        if (!m || n == *m) {
            return factorial(n);
        } else {
            return factorial(n) / factorial(n - *m);
        }
    }

    static int countAll(int n) {
        int total = 0;
        for (int i = 1; i <= n; ++i) {
            total += count(n, std::optional<int>(i));
        }
        return total;
    }

    std::vector<List> select(std::optional<int> m) {
        if (datas == nullptr) {
            throw std::runtime_error("NullPointerException: datas is null");
        }
        if (!m) {
            m = static_cast<int>(datas->size());
        }
        std::vector<List> result;
        List prefix;
        List remaining(*datas);
        selectPermutations(prefix, remaining, *m, result);
        return result;
    }

    std::vector<List> selectAll() {
        if (datas == nullptr) {
            throw std::runtime_error("NullPointerException: datas is null");
        }
        std::vector<List> result;
        for (int i = 1; i <= static_cast<int>(datas->size()); ++i) {
            std::vector<List> selected = select(std::optional<int>(i));
            result.insert(result.end(), selected.begin(), selected.end());
        }
        return result;
    }

    static int factorial(int n) {
        int result = 1;
        for (int i = 2; i <= n; ++i) {
            result *= i;
        }
        return result;
    }

private:
    void selectPermutations(List& prefix, List& remaining, int m, std::vector<List>& result) {
        if (static_cast<int>(prefix.size()) == m) {
            result.push_back(prefix);
            return;
        }
        for (int i = 0; i < static_cast<int>(remaining.size()); ++i) {
            List newPrefix = prefix;
            newPrefix.push_back(remaining[i]);
            List newRemaining = remaining;
            newRemaining.erase(newRemaining.begin() + i);
            selectPermutations(newPrefix, newRemaining, m, result);
        }
    }
};