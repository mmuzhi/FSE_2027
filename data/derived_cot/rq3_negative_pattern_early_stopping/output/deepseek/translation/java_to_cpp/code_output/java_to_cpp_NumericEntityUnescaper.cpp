#include <string>
#include <cctype>
#include <stdexcept>

class NumericEntityUnescaper {
public:
    std::string replace(const std::string& string) const {
        std::string out;
        std::size_t pos = 0;
        std::size_t length = string.length();

        while (pos < length - 2) {
            if (string[pos] == '&' && string[pos + 1] == '#') {
                std::size_t start = pos + 2;
                bool isHex = false;
                char firstChar = string[start];

                if (firstChar == 'x' || firstChar == 'X') {
                    ++start;
                    isHex = true;
                }

                if (start == length) {
                    return out;
                }

                std::size_t end = start;
                while (end < length && isHexChar(string[end])) {
                    ++end;
                }

                if (end < length && string[end] == ';') {
                    try {
                        int entityValue = std::stoi(string.substr(start, end - start), nullptr, isHex ? 16 : 10);
                        out.push_back(static_cast<char>(entityValue));
                        pos = end + 1;
                        continue;
                    } catch (const std::exception&) {
                        return out;
                    }
                }
            }
            out.push_back(string[pos]);
            ++pos;
        }

        return out;
    }

    static bool isHexChar(char c) {
        return std::isdigit(c) || ('a' <= std::tolower(c) && std::tolower(c) <= 'f');
    }
};