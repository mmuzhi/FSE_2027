#include <vector>
#include <algorithm>
#include <iostream>

class AvgPartition {
private:
    std::vector<int> lst;
    int limit;

public:
    AvgPartition(const std::vector<int>& lst, int limit) : lst(lst), limit(limit) {}

    std::pair<int, int> setNum() {
        int size = lst.size() / limit;
        int remainder = lst.size() % limit;
        return {size, remainder};
    }

    std::vector<int> get(int index) {
        auto [size, remainder] = setNum();
        int start = index * size + std::min(index, remainder);
        int end = start + size;
        if (index + 1 <= remainder) {
            end += 1;
        }
        return std::vector<int>(lst.begin() + start, lst.begin() + end);
    }
};

int main() {
    std::vector<int> lst = {1, 2, 3, 4};
    AvgPartition a(lst, 2);
    auto v0 = a.get(0);
    for (int x : v0) std::cout << x << " ";
    std::cout << std::endl;
    auto v1 = a.get(1);
    for (int x : v1) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}