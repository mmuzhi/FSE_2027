#include <cctype>
#include <climits>
#include <string>

class NumericEntityUnescaper {
public:
    std::string replace(const std::string& str) const {
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
                    int entityValue = 0;
                    // Mimics Integer.parseInt(...): on "NumberFormatException"
                    // (empty digits, invalid digit for radix, or overflow past
                    // int range) the accumulated output is returned as-is.
                    if (parseInt(str.substr(start, end - start),
                                 isHex ? 16 : 10, entityValue)) {
                        out += static_cast<char>(entityValue);
                        pos = end + 1;
                        continue;
                    } else {
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
        if (std::isdigit(uc) != 0) {
            return true;
        }
        unsigned char lower = static_cast<unsigned char>(std::tolower(uc));
        return 'a' <= lower && lower <= 'f';
    }

private:
    // Equivalent of java.lang.Integer.parseInt(String, int) restricted to the
    // character set accepted by isHexChar. Returns false instead of throwing.
    static bool parseInt(const std::string& s, int radix, int& result) {
        if (s.empty()) {
            return false;
        }
        long long value = 0;
        for (char c : s) {
            int digit;
            if (c >= '0' && c <= '9') {
                digit = c - '0';
            } else if (c >= 'a' && c <= 'f') {
                digit = c - 'a' + 10;
            } else if (c >= 'A' && c <= 'F') {
                digit = c - 'A' + 10;
            } else {
                return false;
            }
            if (digit >= radix) {
                return false;
            }
            if (value > (INT_MAX - digit) / radix) {
                return false; // overflow beyond int range
            }
            value = value * radix + digit;
        }
        result = static_cast<int>(value);
        return true;
    }
};