#include <string>
#include <sstream>
#include <cstdlib> // for abs

class NumberConverter {
public:
    static std::string decimal_to_binary(int decimal_num) {
        if (decimal_num == 0) {
            return "0";
        }
        bool negative = false;
        if (decimal_num < 0) {
            negative = true;
            decimal_num = abs(decimal_num);
        }
        std::string binary;
        while (decimal_num) {
            binary = (decimal_num % 2 ? '1' : '0') + binary;
            decimal_num /= 2;
        }
        if (negative) {
            binary = '-' + binary;
        }
        return binary;
    }

    static int binary_to_decimal(const std::string& binary_str) {
        // We'll handle negative binary strings if any? The problem doesn't specify, but the example is positive.
        // The Python code does not show negative, so we assume positive.
        // But the problem says identical behavior, so if the input binary_str has a minus sign, we should handle it.
        // However, the problem's example input is positive. Let's stick to the requirement: the input is a string of binary digits (without the '0b' prefix) and may be negative.

        // Check if the string starts with '-'
        if (binary_str.empty()) {
            return 0;
        }
        bool negative = false;
        if (binary_str[0] == '-') {
            negative = true;
            binary_str = binary_str.substr(1);
        }

        // If the string is empty after removing the minus, then it's zero.
        if (binary_str.empty()) {
            return 0;
        }

        // We'll convert the binary string to decimal.
        int result = 0;
        for (char c : binary_str) {
            if (c == '0' || c == '1') {
                result = result * 2 + (c - '0');
            } else {
                // This should not happen if the input is valid, but we'll treat invalid characters as 0?
                // The problem doesn't specify, but the Python int(base) would throw an exception for invalid characters.
                // We'll return 0 for invalid characters? Or throw an exception? The problem says identical behavior, so we must throw an exception?
                // But the problem doesn't specify. Let's stick to the Python behavior: if there's an invalid character, it throws a ValueError.
                // However, the problem says "Keep behavior identical", so we must throw an exception for invalid characters.

                // Since we are not required to change behavior, we can throw an exception.
                throw std::invalid_argument("Invalid binary digit");
            }
        }

        if (negative) {
            result = -result;
        }
        return result;
    }

    static std::string decimal_to_octal(int decimal_num) {
        if (decimal_num == 0) {
            return "0";
        }
        bool negative = false;
        if (decimal_num < 0) {
            negative = true;
            decimal_num = abs(decimal_num);
        }
        std::string octal;
        while (decimal_num) {
            int remainder = decimal_num % 8;
            octal = (remainder < 10 ? '0' + remainder : 'A' + (remainder - 10)) + octal;
            decimal_num /= 8;
        }
        if (negative) {
            octal = '-' + octal;
        }
        return octal;
    }

    static int octal_to_decimal(const std::string& octal_str) {
        if (octal_str.empty()) {
            return 0;
        }
        bool negative = false;
        if (octal_str[0] == '-') {
            negative = true;
            octal_str = octal_str.substr(1);
        }

        if (octal_str.empty()) {
            return 0;
        }

        int result = 0;
        for (char c : octal_str) {
            if (c >= '0' && c <= '7') {
                result = result * 8 + (c - '0');
            } else {
                throw std::invalid_argument("Invalid octal digit");
            }
        }

        if (negative) {
            result = -result;
        }
        return result;
    }

    static std::string decimal_to_hex(int decimal_num) {
        if (decimal_num == 0) {
            return "0";
        }
        bool negative = false;
        if (decimal_num < 0) {
            negative = true;
            decimal_num = abs(decimal_num);
        }
        std::string hex_str;
        while (decimal_num) {
            int remainder = decimal_num % 16;
            if (remainder < 10) {
                hex_str = (char)('0' + remainder) + hex_str;
            } else {
                hex_str = (char)('A' + (remainder - 10)) + hex_str;
            }
            decimal_num /= 16;
        }
        if (negative) {
            hex_str = '-' + hex_str;
        }
        return hex_str;
    }

    static int hex_to_decimal(const std::string& hex_str) {
        if (hex_str.empty()) {
            return 0;
        }
        bool negative = false;
        if (hex_str[0] == '-') {
            negative = true;
            hex_str = hex_str.substr(1);
        }

        if (hex_str.empty()) {
            return 0;
        }

        int result = 0;
        for (char c : hex_str) {
            if (c >= '0' && c <= '9') {
                result = result * 16 + (c - '0');
            } else if (c >= 'A' && c <= 'F') {
                result = result * 16 + (c - 'A' + 10);
            } else if (c >= 'a' && c <= 'f') {
                result = result * 16 + (c - 'a' + 10);
            } else {
                throw std::invalid_argument("Invalid hex digit");
            }
        }

        if (negative) {
            result = -result;
        }
        return result;
    }
};