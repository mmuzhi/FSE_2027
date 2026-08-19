#include <algorithm>
#include <cstddef>
#include <stdexcept>
#include <string>

class NumberConverter {
public:
    static std::string decimal_to_binary(long long decimal_num) {
        return to_base(decimal_num, 2, 'b');
    }

    static long long binary_to_decimal(const std::string& binary_num) {
        return from_base(binary_num, 2, 'b');
    }

    static std::string decimal_to_octal(long long decimal_num) {
        return to_base(decimal_num, 8, 'o');
    }

    static long long octal_to_decimal(const std::string& octal_num) {
        return from_base(octal_num, 8, 'o');
    }

    static std::string decimal_to_hex(long long decimal_num) {
        return to_base(decimal_num, 16, 'x');
    }

    static long long hex_to_decimal(const std::string& hex_num) {
        return from_base(hex_num, 16, 'x');
    }

private:
    static const char* kDigits() {
        return "0123456789abcdefghijklmnopqrstuvwxyz";
    }

    [[noreturn]] static void raise_invalid(int base, const std::string& s) {
        // Closest analogue of Python's ValueError
        throw std::invalid_argument(
            "invalid literal for int() with base " + std::to_string(base) +
            ": '" + s + "'");
    }

    // Equivalent of Python bin()/oct()/hex() followed by [2:]:
    //   bin(42423)[2:]   -> "1010010110110111"
    //   bin(-42423)[2:]  -> "b1010010110110111"  (sign and '0' stripped by [2:])
    static std::string to_base(long long value, int base, char prefix_char) {
        const bool negative = value < 0;
        unsigned long long n = negative
            ? -static_cast<unsigned long long>(value)  // magnitude; safe even for LLONG_MIN
            : static_cast<unsigned long long>(value);

        std::string result;
        do {
            result.push_back(kDigits()[n % static_cast<unsigned long long>(base)]);
            n /= static_cast<unsigned long long>(base);
        } while (n > 0);
        std::reverse(result.begin(), result.end());

        if (negative) result.insert(result.begin(), prefix_char);  // Python quirk from [2:]
        return result;
    }

    // Equivalent of Python int(s, base):
    // surrounding whitespace, optional sign, optional matching base prefix
    // ("0b"/"0o"/"0x" in any case) and single underscores between digits are
    // accepted; anything else raises ValueError -> std::invalid_argument.
    static long long from_base(const std::string& s, int base, char prefix_char) {
        std::size_t i = 0, j = s.size();
        auto is_space = [](char c) {
            return c == ' ' || c == '\t' || c == '\n' ||
                   c == '\v' || c == '\f' || c == '\r';
        };
        while (i < j && is_space(s[i])) ++i;
        while (j > i && is_space(s[j - 1])) --j;

        bool negative = false;
        if (i < j && (s[i] == '+' || s[i] == '-')) {
            negative = (s[i] == '-');
            ++i;
        }

        bool prefixed = false;
        if (j - i >= 2 && s[i] == '0' &&
            (s[i + 1] == prefix_char ||
             s[i + 1] == static_cast<char>(prefix_char - 'a' + 'A'))) {
            prefixed = true;
            i += 2;
        }

        unsigned long long acc = 0;
        bool any_digit = false;
        bool allow_underscore = prefixed;  // an underscore may follow the prefix
        for (std::size_t k = i; k < j; ++k) {
            char c = s[k];
            if (c == '_') {
                if (!allow_underscore || k + 1 == j) raise_invalid(base, s);
                allow_underscore = false;
                continue;
            }
            int d;
            if (c >= '0' && c <= '9') d = c - '0';
            else if (c >= 'a' && c <= 'z') d = c - 'a' + 10;
            else if (c >= 'A' && c <= 'Z') d = c - 'A' + 10;
            else raise_invalid(base, s);
            if (d >= base) raise_invalid(base, s);
            any_digit = true;
            allow_underscore = true;
            acc = acc * static_cast<unsigned long long>(base) +
                  static_cast<unsigned long long>(d);
        }
        if (!any_digit) raise_invalid(base, s);

        if (negative) acc = (~acc) + 1ULL;  // two's-complement negate, well-defined
        return static_cast<long long>(acc);
    }
};