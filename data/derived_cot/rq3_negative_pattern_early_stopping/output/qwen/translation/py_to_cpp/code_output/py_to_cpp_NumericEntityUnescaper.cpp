#include <string>
#include <cctype>
#include <cstdlib>
#include <stdexcept>

class NumericEntityUnescaper {
public:
    std::u32string replace(std::u32string string) {
        std::u32string out;
        size_t pos = 0;
        size_t length = string.length();

        while (pos < length - 2) {
            if (string[pos] == '&' && pos+1 < length && string[pos+1] == '#') {
                size_t start = pos + 2;
                bool is_hex = false;
                // Check for 'x' or 'X'
                if (start < length && (string[start] == 'x' || string[start] == 'X')) {
                    start++;
                    is_hex = true;
                }

                // If we are at the end, break.
                if (start == length) {
                    out += string.substr(pos);
                    break;
                }

                // Find the end of the entity value (until non-hex digit or semicolon)
                size_t end = start;
                while (end < length && is_hex_char(string[end])) {
                    end++;
                }

                // Check if we have a semicolon
                if (end < length && string[end] == ';') {
                    try {
                        // Convert the substring from start to end to an integer
                        // We use base 16 if is_hex, else base 10.
                        std::string num_str;
                        if (is_hex) {
                            // Convert the substring to a std::string by taking the code points and converting to char (since they are ASCII)
                            for (size_t i = start; i < end; i++) {
                                char c = static_cast<char>(string[i]);
                                num_str += c;
                            }
                            unsigned long entity_value = std::stoul(num_str, nullptr, is_hex ? 16 : 10);
                            out += static_cast<char32_t>(entity_value);
                            pos = end + 1;
                            continue;
                        } else {
                            // For decimal, we do the same.
                            for (size_t i = start; i < end; i++) {
                                char c = static_cast<char>(string[i]);
                                num_str += c;
                            }
                            unsigned long entity_value = std::stoul(num_str, nullptr, 10);
                            out += static_cast<char32_t>(entity_value);
                            pos = end + 1;
                            continue;
                        }
                    } catch (...) {
                        // If there's an exception, we just append the original string from pos and break.
                        out += string.substr(pos);
                        break;
                    }
                }
            }
            out += string[pos];
            pos++;
        }

        // Append the remaining part of the string
        if (pos < length) {
            out += string.substr(pos);
        }

        return out;
    }

    static bool is_hex_char(char32_t char32) {
        if (char32 >= '0' && char32 <= '9') {
            return true;
        } else if (char32 >= 'a' && char32 <= 'f') {
            return true;
        } else if (char32 >= 'A' && char32 <= 'F') {
            return true;
        }
        return false;
    }
};