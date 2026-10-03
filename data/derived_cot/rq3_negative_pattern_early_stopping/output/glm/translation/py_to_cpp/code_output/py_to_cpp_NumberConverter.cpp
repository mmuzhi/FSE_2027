#include <string>
#include <stdexcept>

class NumberConverter {
private:
    static std::string to_base_unsigned(unsigned long long num, int base) {
        if (num == 0) return "0";
        std::string result;
        while (num > 0) {
            int rem = num % base;
            char c = rem < 10 ? '0' + rem : 'a' + rem - 10;
            result = c + result;
            num /= base;
        }
        return result;
    }

    static long long to_decimal(const std::string& str, int base) {
        if (str.empty()) throw std::invalid_argument("invalid literal");
        size_t i = 0;
        long long sign = 1;
        if (str[0] == '-') {
            sign = -1;
            i = 1;
        } else if (str[0] == '+') {
            i = 1;
        }
        if (i == str.size()) throw std::invalid_argument("invalid literal");
        
        unsigned long long result = 0;
        for (; i < str.size(); ++i) {
            char c = str[i];
            int digit;
            if (c >= '0' && c <= '9') {
                digit = c - '0';
            } else if (c >= 'a' && c <= 'z') {
                digit = c - 'a' + 10;
            } else if (c >= 'A' && c <= 'Z') {
                digit = c - 'A' + 10;
            } else {
                throw std::invalid_argument("invalid literal");
            }
            if (digit >= base) throw std::invalid_argument("invalid literal");
            result = result * base + digit;
        }
        if (sign == -1) {
            return static_cast<long long>(-result);
        }
        return static_cast<long long>(result);
    }

public:
    static std::string decimal_to_binary(long long decimal_num) {
        if (decimal_num == 0) return "0";
        if (decimal_num < 0) {
            unsigned long long mag = static_cast<unsigned long long>(-(decimal_num + 1)) + 1;
            return "b" + to_base_unsigned(mag, 2);
        }
        return to_base_unsigned(static_cast<unsigned long long>(decimal_num), 2);
    }

    static long long binary_to_decimal(const std::string& binary_num) {
        return to_decimal(binary_num, 2);
    }

    static std::string decimal_to_octal(long long decimal_num) {
        if (decimal_num == 0) return "0";
        if (decimal_num < 0) {
            unsigned long long mag = static_cast<unsigned long long>(-(decimal_num + 1)) + 1;
            return "o" + to_base_unsigned(mag, 8);
        }
        return to_base_unsigned(static_cast<unsigned long long>(decimal_num), 8);
    }

    static long long octal_to_decimal(const std::string& octal_num) {
        return to_decimal(octal_num, 8);
    }

    static std::string decimal_to_hex(long long decimal_num) {
        if (decimal_num == 0) return "0";
        if (decimal_num < 0) {
            unsigned long long mag = static_cast<unsigned long long>(-(decimal_num + 1)) + 1;
            return "x" + to_base_unsigned(mag, 16);
        }
        return to_base_unsigned(static_cast<unsigned long long>(decimal_num), 16);
    }

    static long long hex_to_decimal(const std::string& hex_num) {
        return to_decimal(hex_num, 16);
    }
};