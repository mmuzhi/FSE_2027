#include <vector>
#include <algorithm>
#include <utility>

class AvgPartition {
private:
    std::vector<int> lst_;
    int limit_;

public:
    AvgPartition(const std::vector<int>& lst, int limit) : lst_(lst), limit_(limit) {}

    std::pair<int, int> setNum() {
        int size = static_cast<int>(lst_.size()) / limit_;
        int remainder = static_cast<int>(lst_.size()) % limit_;
        return {size, remainder};
    }

    std::vector<int> get(int index) {
        auto [size, remainder] = setNum();
        int start = index * size + std::min(index, remainder);
        int end = start + size;
        if (index + 1 <= remainder) {
            end += 1;
        }
        // Clamp to valid range to mimic Python's slice behavior
        int len = static_cast<int>(lst_.size());
        start = std::min(start, len);
        end = std::min(end, len);
        if (start >= end) {
            return {};
        }
        return std::vector<int>(lst_.begin() + start, lst_.begin() + end);
    }
};