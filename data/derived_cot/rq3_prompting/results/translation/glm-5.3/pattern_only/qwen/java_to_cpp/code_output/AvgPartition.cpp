#include <algorithm>
#include <iostream>
#include <stdexcept>
#include <vector>

class AvgPartition {
private:
    std::vector<int> lst;
    int limit;

public:
    AvgPartition(std::vector<int> lst, int limit)
        : lst(std::move(lst)), limit(limit) {}

    // Java: returns int[]{size, remainder}
    std::vector<int> setNum() const {
        if (limit == 0) {
            // Java throws ArithmeticException("/ by zero") on the division below
            throw std::runtime_error("/ by zero");
        }
        int size = static_cast<int>(lst.size()) / limit;
        int remainder = static_cast<int>(lst.size()) % limit;
        return {size, remainder};
    }

    // Java: returns lst.subList(start, end) (a view); here an equivalent copy.
    std::vector<int> get(int index) const {
        std::vector<int> nums = setNum();
        int size = nums[0];
        int remainder = nums[1];
        int start = index * size + std::min(index, remainder);
        int end = start + size;
        if (index + 1 <= remainder) {
            end += 1;
        }
        // Mirror subList bounds checks (IndexOutOfBoundsException)
        if (start < 0 || end > static_cast<int>(lst.size()) || start > end) {
            throw std::out_of_range("subList index out of bounds");
        }
        return std::vector<int>(lst.begin() + start, lst.begin() + end);
    }
};

// Mirror Java's List toString(): "[1, 2]"
static void printList(const std::vector<int>& v) {
    std::cout << '[';
    for (std::size_t i = 0; i < v.size(); ++i) {
        if (i != 0) std::cout << ", ";
        std::cout << v[i];
    }
    std::cout << "]\n";
}

int main() {
    std::vector<int> lst = {1, 2, 3, 4};
    AvgPartition a(lst, 2);
    printList(a.get(0));
    printList(a.get(1));
    return 0;
}