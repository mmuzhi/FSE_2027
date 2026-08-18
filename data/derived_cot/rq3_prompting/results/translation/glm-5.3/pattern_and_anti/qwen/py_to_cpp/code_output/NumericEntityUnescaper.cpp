#include <string>
#include <stdexcept>

class NumericEntityUnescaper {
public:
    NumericEntityUnescaper() {}

    std::string replace(const std::string& str) const {
        std::string out;
        long long pos = 0;
        long long length = static_cast<long long>(str.size());

        while (pos < length - 2) {
            if (str[pos] == '&' && str[pos + 1] == '#') {
                long long start = pos + 2;
                bool is_hex = false;
                char first_char = str[start];

                if (first_char == 'x' || first_char == 'X') {
                    start += 1;
                    is_hex = true;
                }

                if (start == length) {
                    return out;
                }

                long long end = start;
                while (end < length && is_hex_char(str[end])) {
                    end += 1;
                }

                if (end < length && str[end] == ';') {
                    if (start == end) {
                        // int('') raises -> return partial output
                        return out;
                    }
                    unsigned long long base = is_hex ? 16ULL : 10ULL;
                    unsigned long long entity_value = 0;
                    for (long long i = start; i < end; ++i) {
                        int d = hex_digit_value(str[i]);
                        if (!is_hex && d > 9) {
                            // int(s, 10) with hex letters raises -> return partial output
                            return out;
                        }
                        entity_value = entity_value * base + static_cast<unsigned long long>(d);
                        if (entity_value > 0x10FFFFULL) {
                            // int() succeeds but chr() raises ValueError (uncaught in Python)
                            throw std::runtime_error("chr() arg not in range(0x110000)");
                        }
                    }
                    append_code_point(out, static_cast<unsigned int>(entity_value));
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
        return (c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F');
    }

private:
    static int hex_digit_value(char c) {
        if (c >= '0' && c <= '9') return c - '0';
        if (c >= 'a' && c <= 'f') return c - 'a' + 10;
        if (c >= 'A' && c <= 'F') return c - 'A' + 10;
        return -1;
    }

    static void append_code_point(std::string& out, unsigned int cp) {
        if (cp < 0x80) {
            out += static_cast<char>(cp);
        } else if (cp < 0x800) {
            out += static_cast<char>(0xC0 | (cp >> 6));
            out += static_cast<char>(0x80 | (cp & 0x3F));
        } else if (cp < 0x10000) {
            out += static_cast<char>(0xE0 | (cp >> 12));
            out += static_cast<char>(0x80 | ((cp >> 6) & 0x3F));
            out += static_cast<char>(0x80 | (cp & 0x3F));
        } else {
            out += static_cast<char>(0xF0 | (cp >> 18));
            out += static_cast<char>(0x80 | ((cp >> 12) & 0x3F));
            out += static_cast<char>(0x80 | ((cp >> 6) & 0x3F));
            out += static_cast<char>(0x80 | (cp & 0x3F));
        }
    }
};