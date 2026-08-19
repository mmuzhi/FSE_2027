#include <stdexcept>
#include <string>
#include <vector>

class BitStatusUtil {
public:
    static long long add(long long states, long long stat) {
        check({states, stat});
        return states | stat;
    }

    static bool has(long long states, long long stat) {
        check({states, stat});
        return (states & stat) == stat;
    }

    static long long remove(long long states, long long stat) {
        check({states, stat});
        if (has(states, stat)) {
            return states ^ stat;
        }
        return states;
    }

    static void check(const std::vector<long long>& args) {
        for (long long arg : args) {
            if (arg < 0) {
                throw std::invalid_argument(std::to_string(arg) + " must be greater than or equal to 0");
            }
            if (arg % 2 != 0) {
                throw std::invalid_argument(std::to_string(arg) + " not even");
            }
        }
    }
};