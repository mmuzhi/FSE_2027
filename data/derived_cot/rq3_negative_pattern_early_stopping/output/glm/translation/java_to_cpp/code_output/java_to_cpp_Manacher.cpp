#include <iostream>
#include <string>
#include <algorithm>

class Manacher {
private:
    std::string inputString;

    std::string preprocess(const std::string& s) {
        std::string sb;
        for (int i = 0; i < static_cast<int>(s.length()); i++) {
            sb += '|';
            sb += s[i];
        }
        sb += '|';
        return sb;
    }

protected:
    int palindromicLength(const std::string& s, int center) {
        int diff = 1;
        while (center - diff >= 0 && center + diff < static_cast<int>(s.length()) && s[center - diff] == s[center + diff]) {
            diff++;
        }
        return diff - 1;
    }

public:
    Manacher(const std::string& inputString) {
        this->inputString = inputString;
    }

    std::string palindromicString() {
        std::string processedString = preprocess(inputString);
        int maxLength = 0;
        int centerIndex = 0;

        for (int i = 0; i < static_cast<int>(processedString.length()); i++) {
            int length = palindromicLength(processedString, i);
            if (length > maxLength) {
                maxLength = length;
                centerIndex = i;
            }
        }

        std::string result = processedString.substr(centerIndex - maxLength, 2 * maxLength + 1);
        result.erase(std::remove(result.begin(), result.end(), '|'), result.end());
        return result;
    }
};

int main() {
    Manacher manacher("ababaxse");
    std::cout << manacher.palindromicString() << std::endl;
    return 0;
}