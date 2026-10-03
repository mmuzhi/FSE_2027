#include <string>
#include <cctype> // for isdigit, etc.

class NumericEntityUnescaper {
public:
    std::string replace(const std::string& input) {
        std::string output;
        size_t pos = 0;
        size_t length = input.length();

        while (pos < length - 2) {
            if (input[pos] == '&' && input[pos+1] == '#') {
                size_t start = pos + 2;
                bool isHex = false;
                char firstChar = input[start];

                if (firstChar == 'x' || firstChar == 'X') {
                    start++;
                    isHex = true;
                }

                if (start == length) {
                    // Incomplete entity, return the output so far.
                    return output;
                }

                size_t end = start;
                while (end < length && isHexChar(input[end])) {
                    end++;
                }

                if (end < length && input[end] == ';') {
                    try {
                        std::string numStr = input.substr(start, end - start);
                        long entityValue = std::stol(numStr, nullptr, isHex ? 16 : 10);
                        // Check if the value is within the range of char
                        if (entityValue < 0 || entityValue > 255) {
                            // The original Java code doesn't check, but note: char is typically 8 bits, so 0-255.
                            // However, the Java code uses Integer.parseInt and then casts to char, which might be negative if the system is using signed char and the value is too big.
                            // But the original code doesn't check, so we must not change behavior.
                            // We'll cast anyway, but note: if the value is too big for char, it might be undefined.
                            // Since the problem says to keep behavior identical, we must not change the behavior.
                            // The original Java code would cast any int to char, even if it's out of the char range.
                            // So we do the same.
                            char c = static_cast<char>(entityValue);
                            output.push_back(c);
                            pos = end + 1;
                            continue;
                        } else {
                            char c = static_cast<char>(entityValue);
                            output.push_back(c);
                            pos = end + 1;
                            continue;
                        }
                    } catch (const std::exception& e) {
                        // The original Java code returns the output string on NumberFormatException.
                        return output;
                    }
                }
            }
            output.push_back(input[pos]);
            pos++;
        }

        return output;
    }

    static bool isHexChar(char c) {
        return (c >= '0' && c <= '9') ||
               (c >= 'a' && c <= 'f') ||
               (c >= 'A' && c <= 'F');
    }
};