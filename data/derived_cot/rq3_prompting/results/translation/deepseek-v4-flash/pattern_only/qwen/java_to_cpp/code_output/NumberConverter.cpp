#include <string>
#include <cstdint>
#include <stdexcept>
#include <algorithm>

class NumberConverter {
public:
    static std::string decimalToBinary(int32_t decimalNum) {
        return toUnsignedString(decimalNum, 2);
    }

    static int32_t binaryToDecimal(const std::string& binaryNum) {
        return parseSignedInt(binaryNum, 2);
    }

    static std::string decimalToOctal(int32_t decimalNum) {
        return toUnsignedString(decimalNum, 8);
    }

    static int32_t octalToDecimal(const std::string& octalNum) {
        return parseSignedInt(octalNum, 8);
    }

    static std::string decimalToHex(int32_t decimalNum) {
        return toUnsignedString(decimalNum, 16);
    }

    static int32_t hexToDecimal(const std::string& hexNum) {
        return parseSignedInt(hexNum, 16);
    }

private:
    static std::string toUnsignedString(int32_t value, int radix) {
        uint32_t u = static_cast<uint32_t>(value);
        if (u == 0) return "0";
        const char* digits = "0123456789abcdef";
        std::string result;
        while (u > 0) {
            result.push_back(digits[u % radix]);
            u /= radix;
        }
        std::reverse(result.begin(), result.end());
        return result;
    }

    static int32_t parseSignedInt(const std::string& s, int radix) {
        if (s.empty()) {
            throw std::invalid_argument("NumberFormatException: " + s);
        }
        int i = 0;
        int len = static_cast<int>(s.size());
        bool negative = false;
        int32_t limit = -2147483647;
        if (s[0] < '0') {
            if (s[0] == '-') {
                negative = true;
                limit = -2147483648;
            } else if (s[0] != '+') {
                throw std::invalid_argument("NumberFormatException: " + s);
            }
            if (len == 1) {
                throw std::invalid_argument("NumberFormatException: " + s);
            }
            ++i;
        }
        int32_t multmin = limit / radix;
        int32_t result = 0;
        while (i < len) {
            int digit = charToDigit(s[i++], radix);
            if (digit < 0) {
                throw std::invalid_argument("NumberFormatException: " + s);
            }
            if (result < multmin) {
                throw std::invalid_argument("NumberFormatException: " + s);
            }
            result *= radix;
            if (result < limit + digit) {
                throw std::invalid_argument("NumberFormatException: " + s);
            }
            result -= digit;
        }
        return negative ? result : -result;
    }

    static int charToDigit(char c, int radix) {
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