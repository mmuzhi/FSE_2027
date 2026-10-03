#include <string>
#include <vector>

class Manacher {
public:
    Manacher(const std::string& inputString) : inputString(inputString) {}

    std::string preprocess(const std::string& s) {
        std::string processed;
        processed.reserve(s.length() + 2 * (s.length() + 1));
        for (int i = 0; i < s.length(); ++i) {
            processed.push_back('|');
            processed.push_back(s[i]);
        }
        processed.push_back('|');
        return processed;
    }

    int palindromicLength(const std::string& s, int center) {
        int diff = 1;
        while (center - diff >= 0 && center + diff < static_cast<int>(s.length()) && s[center - diff] == s[center + diff]) {
            ++diff;
        }
        return diff - 1;
    }

    std::string palindromicString() {
        std::string processedString = preprocess(inputString);
        int maxLength = 0;
        int centerIndex = 0;

        for (int i = 0; i < processedString.length(); ++i) {
            int length = palindromicLength(processedString, i);
            if (length > maxLength) {
                maxLength = length;
                centerIndex = i;
            }
        }

        std::string result = processedString.substr(centerIndex - maxLength, 2 * maxLength + 1);
        for (auto it = result.begin(); it != result.end(); ++it) {
            if (*it == '|') {
                it = result.erase(it);
            }
        }
        return result;
    }

    static void main() {
        Manacher manacher("ababaxse");
        std::string result = manacher.palindromicString();
        // For demonstration, print the result. In practice, use appropriate output.
        // std::cout << result << std::endl; // Uncomment if needed
    }
};