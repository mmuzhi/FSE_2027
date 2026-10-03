#include <string>
#include <stdexcept>
#include <climits>

class NumberConverter {
public:
    static std::string decimalToBinary(int decimalNum) {
        if (decimalNum == 0) return "0";
        std::string result;
        unsigned int uNum = static_cast<unsigned int>(decimalNum);
        while (uNum > 0) {
            result = static_cast<char>((uNum % 2) + '0') + result;
            uNum /= 2;
        }
        return result;
    }

    static int binaryToDecimal(std::string binaryNum) {
        return parseInt(binaryNum, 2);
    }

    static std::string decimalToOctal(int decimalNum) {
        if (decimalNum == 0) return "0";
        std::string result;
        unsigned int uNum = static_cast<unsigned int>(decimalNum);
        while (uNum > 0) {
            result = static_cast<char>((uNum % 8) + '0') + result;
            uNum /= 8;
        }
        return result;
    }

    static int octalToDecimal(std::string octalNum) {
        return parseInt(octalNum, 8);
    }

    static std::string decimalToHex(int decimalNum) {
        if (decimalNum == 0) return "0";
        std::string result;
        unsigned int uNum = static_cast<unsigned int>(decimalNum);
        while (uNum > 0) {
            int rem = uNum % 16;
            char c = (rem < 10) ? (rem + '0') : (rem - 10 + 'a');
            result = c + result;
            uNum /= 16;
        }
        return result;
    }

    static int hexToDecimal(std::string hexNum) {
        return parseInt(hexNum, 16);
    }

private:
    static int parseInt(const std::string& s, int radix) {
        if (s.empty()) {
            throw std::invalid_argument("Empty string");
        }
        
        int i = 0;
        bool negative = false;
        
        if (s[0] == '-') {
            negative = true;
            i = 1;
        } else if (s[0] == '+') {
            i = 1;
        }
        
        if (i == static_cast<int>(s.length())) {
            throw std::invalid_argument("Only sign character");
        }
        
        long long limit = negative ? (static_cast<long long>(INT_MAX) + 1) : INT_MAX;
        long long result = 0;
        
        while (i < static_cast<int>(s.length())) {
            int digit = CharacterDigit(s[i], radix);
            if (digit < 0) {
                throw std::invalid_argument("Invalid character");
            }
            if (result > limit / radix) {
                throw std::out_of_range("Out of range");
            }
            result *= radix;
            if (limit - result < digit) {
                throw std::out_of_range("Out of range");
            }
            result += digit;
            i++;
        }
        
        return negative ? -static_cast<int>(result) : static_cast<int>(result);
    }

    static int CharacterDigit(char c, int radix) {
        int digit = -1;
        if (c >= '0' && c <= '9') {
            digit = c - '0';
        } else if (c >= 'A' && c <= 'Z') {
            digit = c - 'A' + 10;
        } else if (c >= 'a' && c <= 'z') {
            digit = c - 'a' + 10;
        }
        return (digit < radix) ? digit : -1;
    }
};