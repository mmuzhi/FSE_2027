#include <vector>
#include <iostream>
#include <algorithm>

class ArrangementCalculator {
private:
    std::vector<void*> datas;

public:
    ArrangementCalculator(std::vector<void*> datas) : datas(datas) {}

    static int count(int n, int* m = nullptr) {
        if (m == nullptr || n == *m) {
            return factorial(n);
        } else {
            return factorial(n) / factorial(n - *m);
        }
    }

    static int countAll(int n) {
        int total = 0;
        for (int i = 1; i <= n; ++i) {
            total += count(n, &i);
        }
        return total;
    }

    std::vector<std::vector<void*>> select(int* m = nullptr) {
        if (m == nullptr) {
            m = new int(datas.size());
        }
        std::vector<std::vector<void*>> result;
        selectPermutations(std::vector<void*>(), datas, *m, result);
        delete m;
        return result;
    }

    std::vector<std::vector<void*>> selectAll() {
        std::vector<std::vector<void*>> result;
        for (int i = 1; i <= datas.size(); ++i) {
            int* m_ptr = new int(i);
            result.insert(result.end(), select(nullptr, m_ptr).begin(), select(nullptr, m_ptr).end());
            delete m_ptr;
        }
        return result;
    }

private:
    static int factorial(int n) {
        int result = 1;
        for (int i = 2; i <= n; ++i) {
            result *= i;
        }
        return result;
    }

    void selectPermutations(std::vector<void*> prefix, std::vector<void*> remaining, int m, std::vector<std::vector<void*>>& result) {
        if (prefix.size() == m) {
            result.push_back(prefix);
            return;
        }
        for (int i = 0; i < remaining.size(); ++i) {
            std::vector<void*> newPrefix = prefix;
            newPrefix.push_back(remaining[i]);
            std::vector<void*> newRemaining = remaining;
            newRemaining.erase(newRemaining.begin() + i);
            selectPermutations(newPrefix, newRemaining, m, result);
        }
    }
};