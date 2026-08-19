#include <string>
#include <cctype>
#include <cstdint>

class NumericEntityUnescaper {
public:
    NumericEntityUnescaper() {}

    // Replaces numeric character references (HTML entities) in the input
    // string with their corresponding Unicode characters (UTF-8 encoded).
    std::string replace(const std::string& str) {
        std::string out;
        size_t pos = 0;
        size_t length = str.size();

        // Python: while pos < length - 2  (written as pos + 2 < length to
        // avoid unsigned underflow when length < 2)
        while (pos + 2 < length) {
            if (str[pos] == '&' && str[pos + 1] == '#') {
                size_t start = pos + 2;
                bool is_hex = false;
                char first_char = str[start];

                if (first_char == 'x' || first_char == 'X') {
                    start += 1;
                    is_hex = true;
                }

                if (start == length) {
                    return out;
                }

                size_t end = start;
                while (end < length && is_hex_char(str[end])) {
                    end += 1;
                }

                if (end < length && str[end] == ';') {
                    // Python: int(string[start:end], base) inside try/except;
                    // on any failure it returns the accumulated output.
                    std::string digits = str.substr(start, end - start);
                    unsigned long long entity_value = 0;
                    if (!parse_number(digits, is_hex ? 16 : 10, entity_value)) {
                        return out;
                    }
                    // chr() raises ValueError (caught by bare except) for
                    // code points above 0x10FFFF
                    if (entity_value > 0x10FFFFULL) {
                        return out;
                    }
                    append_utf8(out, static_cast<std::uint32_t>(entity_value));
                    pos = end + 1;
                    continue;
                }
            }

            out.push_back(str[pos]);
            pos += 1;
        }

        return out;
    }

    // Determines whether a given character is a hexadecimal digit.
    static bool is_hex_char(char c) {
        unsigned char u = static_cast<unsigned char>(c);
        if (std::isdigit(u)) {
            return true;
        }
        unsigned char l = static_cast<unsigned char>(std::tolower(u));
        return 'a' <= l && l <= 'f';
    }

private:
    // Mimics Python's int(s, base) success/failure semantics:
    // empty string, trailing junk (e.g. hex letters under base 10),
    // and overflow all count as failures.
    static bool parse_number(const std::string& s, int base, unsigned long long& value) {
        if (s.empty()) {
            return false;
        }
        try {
            size_t idx = 0;
            value = std::stoull(s, &idx, base);
            return idx == s.size();
        } catch (...) {
            return false;
        }
    }

    static void append_utf8(std::string& out, std::uint32_t cp) {
        if (cp < 0x80) {
            out.push_back(static_cast<char>(cp));
        } else if (cp < 0x800) {
            out.push_back(static_cast<char>(0xC0 | (cp >> 6)));
            out.push_back(static_cast<char>(0x80 | (cp & 0x3F)));
        } else if (cp < 0x10000) {
            out.push_back(static_cast<char>(0xE0 | (cp >> 12)));
            out.push_back(static_cast<char>(0x80 | ((cp >> 6) & 0x3F)));
            out.push_back(static_cast<char>(0x80 | (cp & 0x3F)));
        } else {
            out.push_back(static_cast<char>(0xF0 | (cp >> 18)));
            out.push_back(static_cast<char>(0x80 | ((cp >> 12) & 0x3F)));
            out.push_back(static_cast<char>(0x80 | ((cp >> 6) & 0x3F)));
            out.push_back(static_cast<char>(0x80 | (cp & 0x3F)));
        }
    }
};