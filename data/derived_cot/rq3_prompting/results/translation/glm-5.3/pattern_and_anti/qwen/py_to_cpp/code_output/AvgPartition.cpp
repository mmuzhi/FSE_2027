#include <vector>
#include <utility>
#include <algorithm>

class AvgPartition {
public:
    AvgPartition(std::vector<int> lst, int limit)
        : lst(std::move(lst)), limit(limit) {}

    std::pair<int, int> setNum() const {
        int size = static_cast<int>(lst.size()) / limit;
        int remainder = static_cast<int>(lst.size()) % limit;
        return {size, remainder};
    }

    std::vector<int> get(int index) const {
        auto [size, remainder] = setNum();
        int start = index * size + std::min(index, remainder);
        int end = start + size;
        if (index + 1 <= remainder) {
            end += 1;
        }
        return std::vector<int>(lst.begin() + start, lst.begin() + end);
    }

private:
    std::vector<int> lst;
    int limit;
};