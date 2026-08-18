#include <iostream>
#include <vector>
#include <algorithm>
#include <stdexcept>
#include <string>

class AvgPartition {
private:
    std::vector<int> lst;
    int limit;

public:
    AvgPartition(std::vector<int> lst, int limit)
        : lst(std::move(lst)), limit(limit) {}

    // Equivalent of setNum(): returns {size, remainder}
    std::vector<int> setNum() const {
        int size = static_cast<int>(lst.size()) / limit;
        int remainder = static_cast<int>(lst.size()) % limit;
        return {size, remainder};
    }

    // Equivalent of subList-based get(); returns the slice [start, end)
    std::vector<int> get(int index) const {
        std::vector<int> nums = setNum();
        int size = nums[0];
        int remainder = nums[1];
        int start = index * size + std::min(index, remainder);
        int end = start + size;
        if (index + 1 <= remainder) {
            end += 1;
        }
        // Mimic Java subList bounds checks
        if (start < 0 || end > static_cast<int>(lst.size())) {
            throw std::out_of_range("Index out of range: fromIndex: " +
                                    std::to_string(start) + ", toIndex: " +
                                    std::to_string(end) + ", size: " +
                                    std::to_string(lst.size()));
        }
        if (start > end) {
            throw std::invalid_argument("fromIndex(" + std::to_string(start) +
                                        ") > toIndex(" + std::to_string(end) + ")");
        }
        return std::vector<int>(lst.begin() + start, lst.begin() + end);
    }
};

// Print a vector in Java List.toString() format, e.g. [1, 2]
static void printList(const std::vector<int>& v) {
    std::cout << "[";
    for (std::size_t i = 0; i < v.size(); ++i) {
        if (i > 0) std::cout << ", ";
        std::cout << v[i];
    }
    std::cout << "]" << std::endl;
}

int main() {
    std::vector<int> lst = {1, 2, 3, 4};
    AvgPartition a(lst, 2);
    printList(a.get(0));
    printList(a.get(1));
    return 0;
}