#include <algorithm>
#include <iostream>
#include <string>
#include <utility>

class Manacher {
private:
    std::string inputString;

    std::string preprocess(const std::string& s) const {
        std::string sb;
        sb.reserve(s.size() * 2 + 1);
        for (std::size_t i = 0; i < s.size(); i++) {
            sb += '|';
            sb += s[i];
        }
        sb += '|';
        return sb;
    }

protected:
    int palindromicLength(const std::string& s, int center) const {
        int diff = 1;
        while (center - diff >= 0 && center + diff < static_cast<int>(s.size())
               && s[center - diff] == s[center + diff]) {
            diff++;
        }
        return diff - 1;
    }

public:
    explicit Manacher(std::string inputString_)
        : inputString(std::move(inputString_)) {}

    std::string palindromicString() const {
        const std::string processedString = preprocess(inputString);
        int maxLength = 0;
        int centerIndex = 0;

        for (int i = 0; i < static_cast<int>(processedString.size()); i++) {
            int length = palindromicLength(processedString, i);
            if (length > maxLength) {
                maxLength = length;
                centerIndex = i;
            }
        }

        std::string result = processedString.substr(centerIndex - maxLength,
                                                    static_cast<std::size_t>(maxLength) * 2 + 1);
        // Equivalent of Java's replace("|", "") — remove all '|' characters.
        result.erase(std::remove(result.begin(), result.end(), '|'), result.end());
        return result;
    }
};

int main() {
    Manacher manacher("ababaxse");
    std::cout << manacher.palindromicString() << std::endl;
    return 0;
}