#include <iostream>
#include <stdexcept>
#include <string>
#include <initializer_list>

class BitStatusUtil {
public:
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

    static void check(std::initializer_list<int> args) {
        for (int arg : args) {
            if (arg < 0) {
                throw std::invalid_argument(std::to_string(arg) + " must be greater than or equal to 0");
            }
            if (arg % 2 != 0) {
                throw std::invalid_argument(std::to_string(arg) + " not even");
            }
        }
    }
};

int main() {
    std::cout << BitStatusUtil::add(2, 4) << std::endl;
    std::cout << (BitStatusUtil::has(6, 2) ? "true" : "false") << std::endl;
    std::cout << BitStatusUtil::remove(6, 2) << std::endl;
    try {
        BitStatusUtil::check({2, 3, 4});
    } catch (const std::invalid_argument& e) {
        std::cout << e.what() << std::endl;
    }
    return 0;
}