#include <string>
#include <stdexcept>

namespace org {
namespace example {

class NumericEntityUnescaper {
public:
    // Java String is a UTF-16 code-unit sequence; std::u16string mirrors it
    // (charAt -> operator[], (char) cast -> char16_t truncation mod 2^16).
    std::u16string replace(const std::u16string& string) {
        std::u16string out;
        int pos = 0;
        int length = static_cast<int>(string.length());

        while (pos < length - 2) {
            if (string[pos] == u'&' && string[pos + 1] == u'#') {
                int start = pos + 2;
                bool isHex = false;
                char16_t firstChar = string[start];

                if (firstChar == u'x' || firstChar == u'X') {
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

                if (end < length && string[end] == u';') {
                    try {
                        // substring contains only ASCII hex chars, safe to narrow
                        std::string digits;
                        for (int i = start; i < end; ++i) {
                            digits.push_back(static_cast<char>(string[i]));
                        }
                        // stoi throws invalid_argument (empty/bad) or
                        // out_of_range (overflow) where Java throws
                        // NumberFormatException; both paths return `out`.
                        int entityValue = std::stoi(digits, nullptr, isHex ? 16 : 10);
                        out.push_back(static_cast<char16_t>(entityValue));
                        pos = end + 1;
                        continue;
                    } catch (const std::exception&) {
                        return out;
                    }
                }
            }
            out.push_back(string[pos]);
            pos++;
        }

        return out;
    }

    static bool isHexChar(char16_t c) {
        char16_t lower = (c >= u'A' && c <= u'Z')
                             ? static_cast<char16_t>(c + (u'a' - u'A'))
                             : c;
        return (c >= u'0' && c <= u'9') || (lower >= u'a' && lower <= u'f');
    }
};

} // namespace example
} // namespace org