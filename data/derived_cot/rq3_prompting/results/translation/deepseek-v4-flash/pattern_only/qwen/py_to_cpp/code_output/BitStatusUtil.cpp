#include <cstdint>
#include <stdexcept>
#include <string>
#include <vector>

class BitStatusUtil {
public:
    static int64_t add(int64_t states, int64_t stat) {
        check({states, stat});
        return states | stat;
    }

    static bool has(int64_t states, int64_t stat) {
        check({states, stat});
        return (states & stat) == stat;
    }

    static int64_t remove(int64_t states, int64_t stat) {
        check({states, stat});
        if (has(states, stat)) {
            return states ^ stat;
        }
        return states;
    }

    static void check(const std::vector<int64_t>& args) {
        for (int64_t arg : args) {
            if (arg < 0) {
                throw std::invalid_argument(
                    std::to_string(arg) + " must be greater than or equal to 0");
            }
            if (arg % 2 != 0) {
                throw std::invalid_argument(std::to_string(arg) + " not even");
            }
        }
    }
};