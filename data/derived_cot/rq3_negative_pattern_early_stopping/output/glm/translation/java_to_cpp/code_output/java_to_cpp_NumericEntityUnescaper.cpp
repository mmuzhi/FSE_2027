#include <string>
#include <cctype>
#include <stdexcept>

class NumericEntityUnescaper {
public:
    std::string replace(const std::string& string) {
        std::string out;
        int pos = 0;
        // Cast to int to perfectly mimic Java's signed int arithmetic for length - 2
        // This prevents size_t underflow which would cause an out-of-bounds access in C++
        int length = static_cast<int>(string.length());

        while (pos < length - 2) {
            if (string[pos] == '&' && string[pos + 1] == '#') {
                int start = pos + 2;
                bool isHex = false;
                char firstChar = string[start];

                if (firstChar == 'x' || firstChar == 'X') {
                    start++;
                    isHex = true;
                }

                if (start == length) {
                    return out;
                }

                int end = start;
                while (end < length && isHexChar(string[end])) {
                    end++;
                }

                if (end < length && string[end] == ';') {
                    try {
                        int entityValue = std::stoi(string.substr(start, end - start), nullptr, isHex ? 16 : 10);
                        out += static_cast<char>(entityValue);
                        pos = end + 1;
                        continue;
                    } catch (const std::invalid_argument&) {
                        return out;
                    } catch (const std::out_of_range&) {
                        return out;
                    }
                }
            }
            out += string[pos];
            pos++;
        }

        return out;
    }

    static bool isHexChar(char c) {
        unsigned char uc = static_cast<unsigned char>(c);
        char lower = std::tolower(uc);
        return std::isdigit(uc) || ('a' <= lower && lower <= 'f');
    }
};