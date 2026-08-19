#include <bitset>
#include <cstdint>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>

namespace org::example {

class NumberConverter {
public:
    static std::string decimalToBinary(int decimalNum) {
        // Integer.toBinaryString: unsigned view, no leading zeros, "0" for 0
        std::string bits = std::bitset<32>(
            static_cast<unsigned int>(decimalNum)).to_string();
        std::size_t pos = bits.find_first_not_of('0');
        return pos == std::string::npos ? "0" : bits.substr(pos);
    }

    static int binaryToDecimal(const std::string& binaryNum) {
        return parseInt(binaryNum, 2);
    }

    static std::string decimalToOctal(int decimalNum) {
        // Integer.toOctalString: unsigned view (std::oct emits lowercase digits)
        std::ostringstream oss;
        oss << std::oct << static_cast<unsigned int>(decimalNum);
        return oss.str();
    }

    static int octalToDecimal(const std::string& octalNum) {
        return parseInt(octalNum, 8);
    }

    static std::string decimalToHex(int decimalNum) {
        // Integer.toHexString: unsigned view, lowercase
        std::ostringstream oss;
        oss << std::hex << static_cast<unsigned int>(decimalNum);
        return oss.str();
    }

    static int hexToDecimal(const std::string& hexNum) {
        return parseInt(hexNum, 16);
    }

private:
    // Mirrors Integer.parseInt(String, int) semantics:
    // optional leading '+'/'-', full-string validation (no whitespace,
    // no trailing junk), per-digit overflow checks against the 32-bit
    // int range. NumberFormatException maps to std::invalid_argument
    // with the same-style message.
    static int parseInt(const std::string& s, int radix) {
        if (s.empty()) {
            throw std::invalid_argument("For input string: \"" + s + "\"");
        }
        bool negative = false;
        std::size_t i = 0;
        if (s[0] == '-' || s[0] == '+') {
            negative = (s[0] == '-');
            i = 1;
            if (s.size() == 1) {
                throw std::invalid_argument("For input string: \"" + s + "\"");
            }
        }
        const long long limit = negative
            ? static_cast<long long>(std::numeric_limits<int>::min())
            : static_cast<long long>(std::numeric_limits<int>::max());
        long long result = 0;
        for (; i < s.size(); ++i) {
            int digit = digitValue(s[i], radix);
            if (digit < 0) {
                throw std::invalid_argument("For input string: \"" + s + "\"");
            }
            result = result * radix + (negative ? -digit : digit);
            if (negative ? (result < limit) : (result > limit)) {
                throw std::invalid_argument("For input string: \"" + s + "\"");
            }
        }
        return static_cast<int>(result);
    }

    // Mirrors Character.digit(char, int): -1 for invalid chars/digits >= radix
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
};

} // namespace org::example