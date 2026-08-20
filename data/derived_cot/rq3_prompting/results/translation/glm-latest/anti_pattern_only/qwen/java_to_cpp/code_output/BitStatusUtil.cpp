#include <iostream>
#include <initializer_list>
#include <stdexcept>
#include <string>

namespace org {
namespace example {

void check(std::initializer_list<int> args);

int add(int states, int stat) {
    check({states, stat});
    return states | stat;
}

bool has(int states, int stat) {
    check({states, stat});
    return (states & stat) == stat;
}

int remove(int states, int stat) {
    check({states, stat});
    if (has(states, stat)) {
        return states ^ stat;
    }
    return states;
}

void check(std::initializer_list<int> args) {
    for (int arg : args) {
        if (arg < 0) {
            throw std::invalid_argument(std::to_string(arg) + " must be greater than or equal to 0");
        }
        if (arg % 2 != 0) {
            throw std::invalid_argument(std::to_string(arg) + " not even");
        }
    }
}

}  // namespace example
}  // namespace org

int main() {
    std::cout << org::example::add(2, 4) << "\n";
    std::cout << std::boolalpha << org::example::has(6, 2) << "\n";
    std::cout << org::example::remove(6, 2) << "\n";
    try {
        org::example::check({2, 3, 4});
    } catch (const std::invalid_argument& e) {
        std::cout << e.what() << "\n";
    }
    return 0;
}