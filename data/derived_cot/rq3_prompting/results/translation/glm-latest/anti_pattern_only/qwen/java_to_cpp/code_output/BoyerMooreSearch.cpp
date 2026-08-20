#include <algorithm>
#include <string>
#include <unordered_map>
#include <vector>

namespace org {
namespace example {

class BoyerMooreSearch {
private:
    const std::string text;
    const std::string pattern;
    const int textLen;
    const int patLen;

public:
    BoyerMooreSearch(const std::string& text, const std::string& pattern)
        : text(text),
          pattern(pattern),
          textLen(static_cast<int>(this->text.size())),
          patLen(static_cast<int>(this->pattern.size())) {}

    // Equivalent of Java's String.lastIndexOf(ch)
    int matchInPattern(char ch) const {
        const std::string::size_type pos = pattern.rfind(ch);
        return (pos == std::string::npos) ? -1 : static_cast<int>(pos);
    }

    int mismatchInText(int currentPos) const {
        for (int i = patLen - 1; i >= 0; i--) {
            // .at() preserves the out-of-bounds exception behavior of charAt()
            if (pattern.at(i) != text.at(currentPos + i)) {
                return currentPos + i;
            }
        }
        return -1;
    }

    std::vector<int> badCharacterHeuristic() const {
        std::vector<int> positions;
        int i = 0;

        std::unordered_map<char, int> badCharHeuristic;
        for (int j = 0; j < patLen; j++) {
            badCharHeuristic[pattern.at(j)] = j;
        }

        if (patLen == 0) {
            for (int j = 0; j <= textLen; ++j) {
                positions.push_back(j);
            }
            return positions;
        }

        while (i <= textLen - patLen) {
            const int mismatchIndex = mismatchInText(i);
            if (mismatchIndex == -1) {
                positions.push_back(i);
                i += patLen;
            } else {
                const char mismatchChar = text.at(mismatchIndex);
                const std::unordered_map<char, int>::const_iterator it =
                    badCharHeuristic.find(mismatchChar);
                const int matchIndex =
                    (it != badCharHeuristic.end()) ? it->second : -1;
                if (matchIndex >= 0) {
                    i += std::max(1, mismatchIndex - i - matchIndex);
                } else {
                    i += mismatchIndex - i + 1;
                }
            }
        }
        return positions;
    }
};

}  // namespace example
}  // namespace org