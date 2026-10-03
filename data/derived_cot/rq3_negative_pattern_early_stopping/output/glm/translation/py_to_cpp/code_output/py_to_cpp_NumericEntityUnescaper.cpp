#include <string>
#include <cctype>
#include <stdexcept>

class NumericEntityUnescaper {
public:
    std::string replace(const std::string& str) const {
        std::string out;
        int pos = 0;
        int length = static_cast<int>(str.length());

        while (pos < length - 2) {
            if (str[pos] == '&' && str[pos + 1] == '#') {
                int start = pos + 2;
                bool is_hex = false;
                char first_char = str[start];

                if (first_char == 'x' || first_char == 'X') {
                    start += 1;
                    is_hex = true;
                }

                if (start == length) {
                    return out;
                }

                int end = start;
                while (end < length && is_hex_char(str[end])) {
                    end += 1;
                }

                if (end < length && str[end] == ';') {
                    long long entity_value;
                    try {
                        int base = is_hex ? 16 : 10;
                        std::string num_str = str.substr(start, end - start);
                        entity_value = std::stoll(num_str, nullptr, base);
                    } catch (...) {
                        return out;
                    }

                    // Mimic Python's chr() behavior which throws ValueError for invalid codepoints
                    if (entity_value < 0 || entity_value > 0x10FFFF || (entity_value >= 0xD800 && entity_value <= 0xDFFF)) {
                        throw std::invalid_argument("chr() arg not in range(0x110000)");
                    }
                    append_utf8(out, static_cast<int>(entity_value));
                    pos = end + 1;
                    continue;
                }
            }
            out += str[pos];
            pos += 1;
        }

        return out;
    }

    static bool is_hex_char(char c) {
        unsigned char uc = static_cast<unsigned char>(c);
        return std::isdigit(uc) || ('a' <= std::tolower(uc) && std::tolower(uc) <= 'f');
    }

private:
    static void append_utf8(std::string& out, int codepoint) {
        if (codepoint < 0x80) {
            out += static_cast<char>(codepoint);
        } else if (codepoint < 0x800) {
            out += static_cast<char>(0xC0 | (codepoint >> 6));
            out += static_cast<char>(0x80 | (codepoint & 0x3F));
        } else if (codepoint < 0x10000) {
            out += static_cast<char>(0xE0 | (codepoint >> 12));
            out += static_cast<char>(0x80 | ((codepoint >> 6) & 0x3F));
            out += static_cast<char>(0x80 | (codepoint & 0x3F));
        } else {
            out += static_cast<char>(0xF0 | (codepoint >> 18));
            out += static_cast<char>(0x80 | ((codepoint >> 12) & 0x3F));
            out += static_cast<char>(0x80 | ((codepoint >> 6) & 0x3F));
            out += static_cast<char>(0x80 | (codepoint & 0x3F));
        }
    }
};