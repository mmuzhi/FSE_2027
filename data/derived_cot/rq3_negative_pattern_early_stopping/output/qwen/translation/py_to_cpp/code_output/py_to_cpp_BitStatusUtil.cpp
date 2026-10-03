#include <vector>
#include <stdexcept>
#include <string>

class BitStatusUtil {
public:
    static void check(const std::vector<int>& args) {
        for (int arg : args) {
            if (arg < 0) {
                throw std::invalid_argument(std::string() + arg + " must be greater than or equal to 0");
            }
            if (arg % 2 != 0) {
                throw std::invalid_argument(std::string() + arg + " not even");
            }
        }
    }

    static int add(int states, int stat) {
        check({states, stat});
        return states | stat;
    }

    static bool has(int states, int stat) {
        check({states, stat});
        return (states & stat) == stat;
    }

    static int remove(int states, int stat) {
        check({states, stat});
        if (has(states, stat)) {
            return states ^ stat;
        }
        return states;
    }
};