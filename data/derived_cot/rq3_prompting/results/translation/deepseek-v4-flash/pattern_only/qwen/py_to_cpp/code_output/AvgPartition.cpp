#include <vector>
#include <algorithm>
#include <stdexcept>
#include <utility>

template<typename T>
class AvgPartition {
public:
    AvgPartition(std::vector<T> lst, int limit)
        : lst_(std::move(lst)), limit_(limit) {}

    std::pair<long long, long long> setNum() const {
        long long n = static_cast<long long>(lst_.size());
        long long size = floor_div(n, limit_);
        long long remainder = mod(n, limit_);
        return {size, remainder};
    }

    std::vector<T> get(int index) const {
        std::pair<long long, long long> p = setNum();
        long long size = p.first;
        long long remainder = p.second;
        long long start = static_cast<long long>(index) * size + std::min(static_cast<long long>(index), remainder);
        long long end = start + size;
        if (static_cast<long long>(index) + 1 <= remainder) {
            end += 1;
        }
        return slice(start, end);
    }

private:
    std::vector<T> lst_;
    int limit_;

    static long long floor_div(long long a, long long b) {
        if (b == 0) throw std::runtime_error("integer division or modulo by zero");
        long long q = a / b;
        long long r = a % b;
        if (r != 0 && ((r < 0) != (b < 0))) {
            q -= 1;
        }
        return q;
    }

    static long long mod(long long a, long long b) {
        if (b == 0) throw std::runtime_error("integer division or modulo by zero");
        long long r = a % b;
        if (r != 0 && ((r < 0) != (b < 0))) {
            r += b;
        }
        return r;
    }

    std::vector<T> slice(long long start, long long end) const {
        long long n = static_cast<long long>(lst_.size());
        if (start < 0) start += n;
        if (end < 0) end += n;
        if (start < 0) start = 0;
        if (end < 0) end = 0;
        if (start > n) start = n;
        if (end > n) end = n;
        if (start >= end) return {};
        std::vector<T> result;
        result.reserve(static_cast<size_t>(end - start));
        for (long long i = start; i < end; ++i) {
            result.push_back(lst_[static_cast<size_t>(i)]);
        }
        return result;
    }
};