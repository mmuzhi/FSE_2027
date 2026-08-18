#include <bitset>
#include <climits>
#include <sstream>
#include <stdexcept>
#include <string>

namespace org {
namespace example {

class NumberConverter {
public:
    static std::string decimalToBinary(int decimalNum) {
        // Integer.toBinaryString: unsigned 32-bit view, no leading zeros
        std::string s = std::bitset<32>(static_cast<unsigned int>(decimalNum)).to_string();
        std::string::size_type pos = s.find_first_not_of('0');
        return pos == std::string::npos ? "0" : s.substr(pos);
    }

    static int binaryToDecimal(const std::string& binaryNum) {
        return parseIntRadix(binaryNum, 2);
    }

    static std::string decimalToOctal(int decimalNum) {
        // Integer.toOctalString: unsigned 32-bit view, lowercase digits (no letters here)
        std::ostringstream oss;
        oss << std::oct << static_cast<unsigned int>(decimalNum);
        return oss.str();
    }

    static int octalToDecimal(const std::string& octalNum) {
        return parseIntRadix(octalNum, 8);
    }

    static std::string decimalToHex(int decimalNum) {
        // Integer.toHexString: unsigned 32-bit view, lowercase letters
        std::ostringstream oss;
        oss << std::hex << static_cast<unsigned int>(decimalNum);
        return oss.str();
    }

    static int hexToDecimal(const std::string& hexNum) {
        return parseIntRadix(hexNum, 16);
    }

private:
    // Mirrors Character.digit(char, radix) for ASCII
    static int digitOf(char c, int radix) {
        int d;
        if (c >= '0' && c <= '9') d = c - '0';
        else if (c >= 'A' && c <= 'Z') d = c - 'A' + 10;
        else if (c >= 'a' && c <= 'z') d = c - 'a' + 10;
        else return -1;
        return d < radix ? d : -1;
    }

    // Mirrors Integer.parseInt(String, int):
    // optional +/- sign, per-digit radix validation, range check [-2^31, 2^31-1],
    // throws (analogous to NumberFormatException) on empty/invalid/overflow input.
    static int parseIntRadix(const std::string& s, int radix) {
        if (s.empty())
            throw std::invalid_argument("For input string: \"" + s + "\"");

        std::string::size_type i = 0;
        bool negative = false;
        if (s[0] == '-' || s[0] == '+') {
            negative = (s[0] == '-');
            if (s.size() == 1)
                throw std::invalid_argument("For input string: \"" + s + "\"");
            i = 1;
        }

        const long long limit = negative
            ? -(static_cast<long long>(INT_MIN))  // 2147483648
            : static_cast<long long>(INT_MAX);    // 2147483647

        long long result = 0;
        for (; i < s.size(); ++i) {
            int digit = digitOf(s[i], radix);
            if (digit < 0)
                throw std::invalid_argument("For input string: \"" + s + "\"");
            result = result * radix + digit;
            if (result > limit)
                throw std::invalid_argument("For input string: \"" + s + "\"");
        }

        return negative ? static_cast<int>(-result) : static_cast<int>(result);
    }
};

} // namespace example
} // namespace org