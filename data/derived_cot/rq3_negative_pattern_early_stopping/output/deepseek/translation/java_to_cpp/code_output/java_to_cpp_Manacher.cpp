#include <iostream>
#include <string>
#include <algorithm>

class Manacher {
private:
    std::string inputString;

public:
    Manacher(const std::string& inputString) : inputString(inputString) {}

private:
    std::string preprocess(const std::string& s) {
        std::string processed;
        for (size_t i = 0; i < s.length(); ++i) {
            processed += '|';
            processed += s[i];
        }
        processed += '|';
        return processed;
    }

    int palindromicLength(const std::string& s, int center) {
        int diff = 1;
        while (center - diff >= 0 && center + diff < static_cast<int>(s.length()) && s[center - diff] == s[center + diff]) {
            ++diff;
        }
        return diff - 1;
    }

public:
    std::string palindromicString() {
        std::string processedString = preprocess(inputString);
        int maxLength = 0;
        int centerIndex = 0;

        for (int i = 0; i < static_cast<int>(processedString.length()); ++i) {
            int length = palindromicLength(processedString, i);
            if (length > maxLength) {
                maxLength = length;
                centerIndex = i;
            }
        }

        std::string result = processedString.substr(centerIndex - maxLength, 2 * maxLength + 1);
        std::string finalResult;
        for (char ch : result) {
            if (ch != '|') {
                finalResult += ch;
            }
        }
        return finalResult;
    }
};

int main() {
    Manacher manacher("ababaxse");
    std::cout << manacher.palindromicString() << std::endl;
    return 0;
}