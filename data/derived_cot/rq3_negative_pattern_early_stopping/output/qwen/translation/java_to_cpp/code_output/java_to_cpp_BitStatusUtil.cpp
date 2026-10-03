#include <iostream>
#include <string>
#include <stdexcept>

class IllegalArgumentException : public std::exception {
private:
    std::string message;
public:
    explicit IllegalArgumentException(const std::string& msg) : message(msg) {}
    const char* what() const noexcept override {
        return message.c_str();
    }
};

class BitStatusUtil {
public:
    static int add(int states, int stat) {
        check(states, stat);
        return states | stat;
    }

    static bool has(int states, int stat) {
        check(states, stat);
        return (states & stat) == stat;
    }

    static int remove(int states, int stat) {
        check(states, stat);
        if (has(states, stat)) {
            return states ^ stat;
        }
        return states;
    }

    template<typename... Args>
    static void check(Args... args) {
        int values[sizeof...(Args)] = { static_cast<int>(args)... };
        for (int arg : values) {
            if (arg < 0) {
                throw IllegalArgumentException(std::to_string(arg) + " must be greater than or equal to 0");
            }
            if (arg % 2 != 0) {
                throw IllegalArgumentException(std::to_string(arg) + " not even");
            }
        }
    }
};

int main() {
    std::cout << BitStatusUtil::add(2, 4) << std::endl;
    std::cout << BitStatusUtil::has(6, 2) << std::endl;
    std::cout << BitStatusUtil::remove(6, 2) << std::endl;
    try {
        BitStatusUtil::check(2, 3, 4);
    } catch (const IllegalArgumentException& e) {
        std::cout << e.what() << std::endl;
    }
    return 0;
}