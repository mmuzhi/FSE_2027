#include <iostream>
#include <vector>
#include <algorithm>

class AvgPartition {
private:
    std::vector<int> lst;
    int limit;

public:
    AvgPartition(std::vector<int> lst, int limit) : lst(std::move(lst)), limit(limit) {}

    std::vector<int> setNum() {
        int size = lst.size() / limit;
        int remainder = lst.size() % limit;
        return {size, remainder};
    }

    std::vector<int> get(int index) {
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

void printList(const std::vector<int>& v) {
    std::cout << "[";
    for (size_t i = 0; i < v.size(); ++i) {
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