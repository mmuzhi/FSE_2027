#pragma once

#include <cctype>
#include <string>
#include <stdexcept>

namespace org::example {

class NumericEntityUnescaper {
public:
    std::string replace(const std::string& str) {
        std::string out;
        int pos = 0;
        int length = static_cast<int>(str.length());

        while (pos < length - 2) {
            if (str[pos] == '&' && str[pos + 1] == '#') {
                int start = pos + 2;
                bool isHex = false;
                char firstChar = str[start];

                if (firstChar == 'x' || firstChar == 'X') {
                    start++;
                    isHex = true;
                }

                if (start == length) {
                    return out;
                }

                int end = start;
                while (end < length && isHexChar(str[end])) {
                    end++;
                }

                if (end < length && str[end] == ';') {
                    try {
                        int entityValue = std::stoi(str.substr(start, end - start),
                                                    nullptr,
                                                    isHex ? 16 : 10);
                        out += static_cast<char>(entityValue);
                        pos = end + 1;
                        continue;
                    } catch (const std::exception&) {
                        // Covers std::invalid_argument / std::out_of_range,
                        // matching NumberFormatException handling.
                        return out;
                    }
                }
            }
            out += str[pos];
            pos++;
        }

        return out;
    }

    static bool isHexChar(char c) {
        unsigned char uc = static_cast<unsigned char>(c);
        return std::isdigit(uc) != 0 ||
               ('a' <= std::tolower(uc) && std::tolower(uc) <= 'f');
    }
};

} // namespace org::example