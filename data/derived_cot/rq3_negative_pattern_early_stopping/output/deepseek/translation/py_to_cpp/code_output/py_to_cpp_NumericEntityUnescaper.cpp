#include <string>
#include <cctype>
#include <stdexcept>

class NumericEntityUnescaper {
public:
    std::string replace(const std::string& str) {
        std::string out;
        size_t pos = 0;
        size_t length = str.size();

        while (pos + 2 < length) {
            if (str[pos] == '&' && str[pos + 1] == '#') {
                size_t start = pos + 2;
                bool is_hex = false;

                if (start < length) {
                    char first_char = str[start];
                    if (first_char == 'x' || first_char == 'X') {
                        ++start;
                        is_hex = true;
                    }
                }

                if (start >= length) {
                    return out;
                }

                size_t end = start;
                while (end < length && is_hex_char(str[end])) {
                    ++end;
                }

                if (end < length && str[end] == ';') {
                    try {
                        int entity_value = std::stoi(str.substr(start, end - start), nullptr, is_hex ? 16 : 10);
                        out.push_back(static_cast<char>(entity_value));
                        pos = end + 1;
                        continue;
                    } catch (const std::exception&) {
                        return out;
                    }
                }
            }
            out.push_back(str[pos]);
            ++pos;
        }

        while (pos < length) {
            out.push_back(str[pos]);
            ++pos;
        }
        return out;
    }

    static bool is_hex_char(char ch) {
        return std::isxdigit(static_cast<unsigned char>(ch)) != 0;
    }
};