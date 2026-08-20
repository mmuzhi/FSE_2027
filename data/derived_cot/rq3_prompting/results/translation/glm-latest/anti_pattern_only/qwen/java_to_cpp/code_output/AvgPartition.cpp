#include <algorithm>
#include <iostream>
#include <vector>

class AvgPartition {
private:
    std::vector<int> lst;
    int limit;

public:
    AvgPartition(std::vector<int> list, int limit)
        : lst(std::move(list)), limit(limit) {}

    // Equivalent of Java's setNum(): returns {size, remainder}
    std::vector<int> setNum() const {
        int n = static_cast<int>(lst.size());
        int size = n / limit;
        int remainder = n % limit;
        return std::vector<int>{size, remainder};
    }

    // Equivalent of Java's subList-based get(): returns the slice [start, end)
    std::vector<int> get(int index) const {
        std::vector<int> nums = setNum();
        int size = nums[0];
        int remainder = nums[1];
        int start = index * size + std::min(index, remainder);
        int end = start + size;
        if (index + 1 <= remainder) {
            end += 1;
        }
        return std::vector<int>(lst.begin() + start, lst.begin() + end);
    }
};

namespace {
// Prints a vector the way Java prints a List, e.g. [1, 2]
void printList(const std::vector<int>& v) {
    std::cout << '[';
    for (std::size_t i = 0; i < v.size(); ++i) {
        if (i != 0) std::cout << ", ";
        std::cout << v[i];
    }
    std::cout << ']';
}
} // namespace

int main() {
    std::vector<int> lst;
    lst.push_back(1);
    lst.push_back(2);
    lst.push_back(3);
    lst.push_back(4);
    AvgPartition a(lst, 2);
    printList(a.get(0));
    std::cout << '\n';
    printList(a.get(1));
    std::cout << '\n';
    return 0;
}