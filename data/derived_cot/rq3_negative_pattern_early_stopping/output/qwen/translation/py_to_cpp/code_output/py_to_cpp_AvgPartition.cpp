#include <vector>
#include <stdexcept>

class AvgPartition {
private:
    std::vector<int> lst;
    int limit;

public:
    AvgPartition(const std::vector<int>& lst, int limit) : lst(lst), limit(limit) {}

    std::pair<int, int> setNum() {
        if (limit <= 0) {
            throw std::invalid_argument("Limit must be greater than 0");
        }
        int size = lst.size() / limit;
        int remainder = lst.size() % limit;
        return std::make_pair(size, remainder);
    }

    std::vector<int> get(int index) {
        auto [size, remainder] = setNum();
        int start = index * size + (index < remainder ? index : remainder);
        int end = start + size;
        if (index + 1 <= remainder) {
            end++;
        }
        return std::vector<int>(lst.begin() + start, lst.begin() + end);
    }
};