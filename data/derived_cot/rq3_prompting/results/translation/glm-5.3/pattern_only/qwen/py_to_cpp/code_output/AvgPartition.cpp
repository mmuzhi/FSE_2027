#include <vector>
#include <utility>
#include <algorithm>
#include <stdexcept>
#include <string>

class AvgPartition {
public:
    AvgPartition(std::vector<int> lst, int limit)
        : lst(std::move(lst)), limit(limit) {}

    // Returns (size, remainder), matching Python's tuple return.
    std::pair<int, int> setNum() const {
        if (limit == 0) {
            // Python raises ZeroDivisionError here.
            throw std::runtime_error("integer division or modulo by zero");
        }
        int size = floorDiv(static_cast<int>(lst.size()), limit);
        int remainder = floorMod(static_cast<int>(lst.size()), limit);
        return {size, remainder};
    }

    // Returns the block corresponding to partition `index` (a new list, like Python slicing).
    std::vector<int> get(int index) const {
        std::pair<int, int> sr = setNum();
        int size = sr.first;
        int remainder = sr.second;
        int start = index * size + std::min(index, remainder);
        int end = start + size;
        if (index + 1 <= remainder) {
            end += 1;
        }
        return pySlice(start, end);
    }

private:
    std::vector<int> lst;
    int limit;

    // Python floor division (//), which floors rather than truncates.
    static int floorDiv(int a, int b) {
        int q = a / b;
        if ((a % b != 0) && ((a < 0) != (b < 0))) {
            --q;
        }
        return q;
    }

    // Python modulo (%), result takes the sign of the divisor.
    static int floorMod(int a, int b) {
        return a - floorDiv(a, b) * b;
    }

    // Emulates Python lst[start:end] semantics (negative indices wrap, bounds clamp).
    std::vector<int> pySlice(int start, int end) const {
        int n = static_cast<int>(lst.size());
        if (start < 0) start += n;
        if (end < 0) end += n;
        start = std::max(0, std::min(start, n));
        end = std::max(0, std::min(end, n));
        if (start >= end) {
            return {};
        }
        return std::vector<int>(lst.begin() + start, lst.begin() + end);
    }
};