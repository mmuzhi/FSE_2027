#include <algorithm>
#include <cctype>
#include <cstdint>
#include <stdexcept>
#include <string>

class NumberConverter {
public:
    // Convert a number from decimal format to binary format.
    // e.g. decimal_to_binary(42423) == "1010010110110111"
    static std::string decimal_to_binary(long long decimal_num) {
        return to_base(decimal_num, 2);
    }

    // Convert a number from binary format to decimal format.
    // e.g. binary_to_decimal("1010010110110111") == 42423
    static long long binary_to_decimal(const std::string& binary_num) {
        return from_base(binary_num, 2);
    }

    // Convert a number from decimal format to octal format.
    // e.g. decimal_to_octal(42423) == "122667"
    static std::string decimal_to_octal(long long decimal_num) {
        return to_base(decimal_num, 8);
    }

    // Convert a number from octal format to decimal format.
    // e.g. octal_to_decimal("122667") == 42423
    static long long octal_to_decimal(const std::string& octal_num) {
        return from_base(octal_num, 8);
    }

    // Convert a number from decimal format to hex format (lowercase).
    // e.g. decimal_to_hex(42423) == "a5b7"
    static std::string decimal_to_hex(long long decimal_num) {
        return to_base(decimal_num, 16);
    }

    // Convert a number from hex format to decimal format.
    // e.g. hex_to_decimal("a5b7") == 42423
    static long long hex_to_decimal(const std::string& hex_num) {
        return from_base(hex_num, 16);
    }

private:
    static const char* digits() { return "0123456789abcdef"; }

    static std::string to_base(long long value, int base) {
        if (value == 0) return "0";
        const bool negative = value < 0;
        // Two's-complement negation is safe even for LLONG_MIN.
        std::uint64_t n = negative
            ? ~static_cast<std::uint64_t>(value) + 1
            : static_cast<std::uint64_t>(value);
        std::string result;
        while (n != 0) {
            result.push_back(digits()[n % base]);
            n /= base;
        }
        if (negative) result.push_back('-');
        std::reverse(result.begin(), result.end());
        return result;
    }

    // Mirrors Python's int(s, base): optional sign, surrounding whitespace
    // ignored; invalid input raises (std::invalid_argument / std::out_of_range
    // stand in for Python's ValueError).
    static long long from_base(const std::string& num, int base) {
        std::size_t pos = 0;
        const long long result = std::stoll(num, &pos, base);
        // std::stoll ignores trailing garbage; Python does not, so verify the
        // remainder is whitespace only.
        while (pos < num.size() &&
               std::isspace(static_cast<unsigned char>(num[pos]))) {
            ++pos;
        }
        if (pos != num.size()) {
            throw std::invalid_argument("NumberConverter: invalid literal");
        }
        return result;
    }
};