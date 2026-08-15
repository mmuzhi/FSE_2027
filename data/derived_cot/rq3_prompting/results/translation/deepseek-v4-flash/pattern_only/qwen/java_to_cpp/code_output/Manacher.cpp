#include <iostream>
#include <string>

class Manacher {
private:
    std::string inputString;

    std::string preprocess(const std::string& s) {
        std::string sb;
        for (char c : s) {
            sb.push_back('|');
            sb.push_back(c);
        }
        sb.push_back('|');
        return sb;
    }

protected:
    int palindromicLength(const std::string& s, int center) {
        int diff = 1;
        int n = static_cast<int>(s.length());
        while (center - diff >= 0 && center + diff < n &&
               s[center - diff] == s[center + diff]) {
            diff++;
        }
        return diff - 1;
    }

public:
    Manacher(const std::string& inputString) : inputString(inputString) {}

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

        std::string raw = processedString.substr(
            centerIndex - maxLength, 2 * maxLength + 1);

        std::string result;
        for (char c : raw) {
            if (c != '|') {
                result += c;
            }
        }
        return result;
    }
};

int main() {
    Manacher manacher("ababaxse");
    std::cout << manacher.palindromicString() << std::endl;
    return 0;
}