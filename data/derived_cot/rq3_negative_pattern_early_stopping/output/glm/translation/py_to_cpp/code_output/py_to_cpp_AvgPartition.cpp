#include <vector>
#include <utility>
#include <stdexcept>
#include <algorithm>

class AvgPartition {
private:
    std::vector<int> lst;
    int limit;

public:
    AvgPartition(std::vector<int> lst, int limit) : lst(std::move(lst)), limit(limit) {
        if (limit == 0) {
            throw std::invalid_argument("limit cannot be zero");
        }
    }

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

        int list_size = static_cast<int>(lst.size());
        
        if (start >= list_size) {
            return {};
        }
        if (start < 0) {
            start = 0;
        }
        if (end > list_size) {
            end = list_size;
        }
        if (end < start) {
            return {};
        }

        return std::vector<int>(lst.begin() + start, lst.begin() + end);
    }
};