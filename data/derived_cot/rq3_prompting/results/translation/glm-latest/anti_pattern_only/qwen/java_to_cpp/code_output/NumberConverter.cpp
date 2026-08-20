#include <algorithm>
#include <cstddef>
#include <stdexcept>
#include <string>

namespace org {
namespace example {

// Equivalent of java.lang.NumberFormatException.
class NumberFormatException : public std::invalid_argument {
public:
    explicit NumberFormatException(const std::string& message)
        : std::invalid_argument(message) {}
};

class NumberConverter {
public:
    static std::string decimalToBinary(int decimalNum) {
        return toUnsignedString(static_cast<unsigned int>(decimalNum), 2);
    }

    static int binaryToDecimal(const std::string& binaryNum) {
        return parseInt(binaryNum, 2);
    }

    static std::string decimalToOctal(int decimalNum) {
        return toUnsignedString(static_cast<unsigned int>(decimalNum), 8);
    }

    static int octalToDecimal(const std::string& octalNum) {
        return parseInt(octalNum, 8);
    }

    static std::string decimalToHex(int decimalNum) {
        return toUnsignedString(static_cast<unsigned int>(decimalNum), 16);
    }

    static int hexToDecimal(const std::string& hexNum) {
        return parseInt(hexNum, 16);
    }

private:
    // Equivalent of Integer.toBinaryString / toOctalString / toHexString:
    // the value is treated as an unsigned 32-bit integer.
    static std::string toUnsignedString(unsigned int value, int radix) {
        static constexpr char digits[] = "0123456789abcdefghijklmnopqrstuvwxyz";
        if (value == 0) {
            return "0";
        }
        std::string result;
        while (value > 0) {
            result.push_back(digits[value % static_cast<unsigned int>(radix)]);
            value /= static_cast<unsigned int>(radix);
        }
        std::reverse(result.begin(), result.end());
        return result;
    }

    // Equivalent of Character.digit(char, int) for ASCII input.
    static int digitValue(char c, int radix) {
        int digit;
        if (c >= '0' && c <= '9') {
            digit = c - '0';
        } else if (c >= 'a' && c <= 'z') {
            digit = c - 'a' + 10;
        } else if (c >= 'A' && c <= 'Z') {
            digit = c - 'A' + 10;
        } else {
            return -1;
        }
        return digit < radix ? digit : -1;
    }

    static NumberFormatException forInputString(const std::string& s) {
        return NumberFormatException("For input string: \"" + s + "\"");
    }

    // Equivalent of Integer.parseInt(String, int): an optional sign
    // character followed by digits of the given radix; the result must fit
    // in a signed 32-bit int, otherwise NumberFormatException is thrown.
    static int parseInt(const std::string& s, int radix) {
        if (s.empty()) {
            throw forInputString(s);
        }
        std::size_t i = 0;
        bool negative = false;
        if (s[0] == '+' || s[0] == '-') {
            negative = (s[0] == '-');
            ++i;
        }
        if (i == s.size()) {
            throw forInputString(s);
        }
        const long long limit = negative ? 2147483648LL : 2147483647LL;
        long long result = 0;
        for (; i < s.size(); ++i) {
            const int digit = digitValue(s[i], radix);
            if (digit < 0) {
                throw forInputString(s);
            }
            if (result > (limit - digit) / radix) {
                throw forInputString(s);
            }
            result = result * radix + digit;
        }
        return negative ? static_cast<int>(-result) : static_cast<int>(result);
    }
};

} // namespace example
} // namespace org