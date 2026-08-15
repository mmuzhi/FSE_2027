#include <iostream>
#include <vector>
#include <utility>
#include <algorithm>
#include <stdexcept>

class SubList {
    std::vector<int>& ref;
    int start;
    int end;

public:
    SubList(std::vector<int>& ref, int start, int end)
        : ref(ref), start(start), end(end) {}

    friend std::ostream& operator<<(std::ostream& os, const SubList& sl) {
        os << "[";
        for (int i = sl.start; i < sl.end; ++i) {
            if (i != sl.start) os << ", ";
            os << sl.ref[i];
        }
        os << "]";
        return os;
    }
};

class AvgPartition {
    std::vector<int>& lst;
    int limit;

public:
    AvgPartition(std::vector<int>& lst, int limit)
        : lst(lst), limit(limit) {}

    std::pair<int, int> setNum() {
        if (limit == 0) throw std::invalid_argument("division by zero");
        int size = static_cast<int>(lst.size()) / limit;
        int remainder = static_cast<int>(lst.size()) % limit;
        return {size, remainder};
    }

    SubList get(int index) {
        auto nums = setNum();
        int size = nums.first;
        int remainder = nums.second;

        int start = index * size + std::min(index, remainder);
        int end = start + size;

        if (index + 1 <= remainder) {
            end += 1;
        }

        if (start < 0 || end > static_cast<int>(lst.size()) || start > end) {
            throw std::out_of_range("Index out of bounds");
        }

        return SubList(lst, start, end);
    }
};

int main() {
    std::vector<int> lst = {1, 2, 3, 4};
    AvgPartition a(lst, 2);

    std::cout << a.get(0) << std::endl;
    std::cout << a.get(1) << std::endl;

    return 0;
}