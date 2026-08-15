#include <string>
#include <algorithm>
#include <cctype>
#include <stdexcept>
#include <climits>

class NumberConverter {
public:
    static std::string decimal_to_binary(long long decimal_num) {
        if (decimal_num >= 0) {
            return to_base(static_cast<unsigned long long>(decimal_num), 2);
        } else {
            unsigned long long mag = -static_cast<unsigned long long>(decimal_num);
            return "b" + to_base(mag, 2);
        }
    }

    static long long binary_to_decimal(const std::string& binary_num) {
        return parse_int(binary_num, 2);
    }

    static std::string decimal_to_octal(long long decimal_num) {
        if (decimal_num >= 0) {
            return to_base(static_cast<unsigned long long>(decimal_num), 8);
        } else {
            unsigned long long mag = -static_cast<unsigned long long>(decimal_num);
            return "o" + to_base(mag, 8);
        }
    }

    static long long octal_to_decimal(const std::string& octal_num) {
        return parse_int(octal_num, 8);
    }

    static std::string decimal_to_hex(long long decimal_num) {
        if (decimal_num >= 0) {
            return to_base(static_cast<unsigned long long>(decimal_num), 16);
        } else {
            unsigned long long mag = -static_cast<unsigned long long>(decimal_num);
            return "x" + to_base(mag, 16);
        }
    }

    static long long hex_to_decimal(const std::string& hex_num) {
        return parse_int(hex_num, 16);
    }

private:
    static std::string to_base(unsigned long long num, int base) {
        if (num == 0) return "0";
        const char* hex_digits = "0123456789abcdef";
        std::string digits;
        while (num > 0) {
            int rem = num % base;
            if (base == 16) {
                digits.push_back(hex_digits[rem]);
            } else {
                digits.push_back('0' + rem);
            }
            num /= base;
        }
        std::reverse(digits.begin(), digits.end());
        return digits;
    }

    static int char_to_digit(char c) {
        if (c >= '0' && c <= '9') return c - '0';
        if (c >= 'a' && c <= 'f') return c - 'a' + 10;
        if (c >= 'A' && c <= 'F') return c - 'A' + 10;
        return -1;
    }

    static long long parse_int(const std::string& s, int base) {
        size_t i = 0;

        // leading whitespace
        while (i < s.size() && std::isspace(static_cast<unsigned char>(s[i]))) {
            ++i;
        }
        if (i == s.size()) {
            throw std::invalid_argument("invalid literal for int() with base " + std::to_string(base));
        }

        bool negative = false;
        if (s[i] == '+' || s[i] == '-') {
            negative = (s[i] == '-');
            ++i;
        }

        // optional base prefix
        if (i + 1 < s.size() && s[i] == '0') {
            char c = std::tolower(static_cast<unsigned char>(s[i + 1]));
            if ((base == 2 && c == 'b') ||
                (base == 8 && c == 'o') ||
                (base == 16 && c == 'x')) {
                i += 2;
            }
        }

        if (i >= s.size()) {
            throw std::invalid_argument("invalid literal for int() with base " + std::to_string(base));
        }

        unsigned long long result = 0;
        bool any_digit = false;

        while (i < s.size()) {
            char c = s[i];

            // trailing whitespace is allowed only at the end
            if (std::isspace(static_cast<unsigned char>(c))) {
                ++i;
                while (i < s.size() && std::isspace(static_cast<unsigned char>(s[i]))) {
                    ++i;
                }
                if (i != s.size()) {
                    throw std::invalid_argument("invalid literal for int() with base " + std::to_string(base));
                }
                break;
            }

            int digit = char_to_digit(c);
            if (digit < 0 || digit >= base) {
                throw std::invalid_argument("invalid literal for int() with base " + std::to_string(base));
            }

            if (result > (ULLONG_MAX - static_cast<unsigned long long>(digit)) / static_cast<unsigned long long>(base)) {
                throw std::out_of_range("int too big to convert");
            }

            result = result * static_cast<unsigned long long>(base) + static_cast<unsigned long long>(digit);
            any_digit = true;
            ++i;
        }

        if (!any_digit) {
            throw std::invalid_argument("invalid literal for int() with base " + std::to_string(base));
        }

        if (negative) {
            if (result > static_cast<unsigned long long>(LLONG_MAX) + 1ULL) {
                throw std::out_of_range("int too big to convert");
            }
            if (result == static_cast<unsigned long long>(LLONG_MAX) + 1ULL) {
                return LLONG_MIN;
            }
            return -static_cast<long long>(result);
        } else {
            if (result > static_cast<unsigned long long>(LLONG_MAX)) {
                throw std::out_of_range("int too big to convert");
            }
            return static_cast<long long>(result);
        }
    }
};