#include <algorithm>
#include <stdexcept>
#include <utility>
#include <vector>

class AvgPartition {
private:
    std::vector<int> lst;
    int limit;

    // Python-style floor division; mimics ZeroDivisionError for a zero divisor.
    static int floorDiv(int a, int b) {
        if (b == 0) {
            throw std::runtime_error("integer division or modulo by zero");
        }
        int q = a / b;
        int r = a % b;
        if (r != 0 && ((a < 0) != (b < 0))) {
            --q;  // C++ truncates toward zero; Python floors.
        }
        return q;
    }

    // Python-style modulo (result takes the sign of the divisor).
    static int floorMod(int a, int b) {
        return a - floorDiv(a, b) * b;
    }

    // Python-style lst[start:end] slice (step 1): negative indices wrap,
    // bounds are clamped, and an empty vector is returned when start >= end.
    std::vector<int> slice(int start, int end) const {
        int n = static_cast<int>(lst.size());
        if (start < 0) {
            start += n;
            if (start < 0) start = 0;
        } else if (start > n) {
            start = n;
        }
        if (end < 0) {
            end += n;
            if (end < 0) end = 0;
        } else if (end > n) {
            end = n;
        }
        if (start >= end) {
            return {};
        }
        return std::vector<int>(lst.begin() + start, lst.begin() + end);
    }

public:
    // Initialize the class with the given list and the number of partitions.
    AvgPartition(const std::vector<int>& lst, int limit)
        : lst(lst), limit(limit) {}

    // Calculate the size of each block and the remainder of the division.
    // Returns {size, remainder}, mirroring the Python tuple.
    std::pair<int, int> setNum() const {
        int size = floorDiv(static_cast<int>(lst.size()), limit);
        int remainder = floorMod(static_cast<int>(lst.size()), limit);
        return std::make_pair(size, remainder);
    }

    // Calculate start/end positions for the given partition index and
    // return the corresponding block.
    std::vector<int> get(int index) const {
        auto [size, remainder] = setNum();
        int start = index * size + std::min(index, remainder);
        int end = start + size;
        if (index + 1 <= remainder) {
            end += 1;
        }
        return slice(start, end);
    }
};