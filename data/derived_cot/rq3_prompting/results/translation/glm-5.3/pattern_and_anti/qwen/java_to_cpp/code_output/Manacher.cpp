#include <iostream>
#include <string>
#include <algorithm>

class Manacher {
private:
    std::string inputString;

public:
    explicit Manacher(const std::string& inputString) : inputString(inputString) {}

private:
    std::string preprocess(const std::string& s) {
        std::string result;
        for (std::size_t i = 0; i < s.length(); i++) {
            result += '|';
            result += s[i];
        }
        result += '|';
        return result;
    }

protected:
    int palindromicLength(const std::string& s, int center) {
        int diff = 1;
        int len = static_cast<int>(s.length());
        while (center - diff >= 0 && center + diff < len
               && s[center - diff] == s[center + diff]) {
            diff++;
        }
        return diff - 1;
    }

public:
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