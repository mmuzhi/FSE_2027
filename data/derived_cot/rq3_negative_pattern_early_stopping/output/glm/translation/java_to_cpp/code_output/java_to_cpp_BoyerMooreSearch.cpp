#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>

class BoyerMooreSearch {
private:
    const std::string text;
    const std::string pattern;
    const int textLen;
    const int patLen;

public:
    BoyerMooreSearch(const std::string& text, const std::string& pattern)
        : text(text), pattern(pattern),
          textLen(static_cast<int>(text.length())),
          patLen(static_cast<int>(pattern.length())) {}

    int matchInPattern(char ch) const {
        size_t pos = pattern.rfind(ch);
        return (pos == std::string::npos) ? -1 : static_cast<int>(pos);
    }

    int mismatchInText(int currentPos) const {
        for (int i = patLen - 1; i >= 0; i--) {
            if (pattern[i] != text[currentPos + i]) {
                return currentPos + i;
            }
        }
        return -1;
    }

    std::vector<int> badCharacterHeuristic() {
        std::vector<int> positions;
        int i = 0;

        std::unordered_map<char, int> badCharHeuristic;
        for (int j = 0; j < patLen; j++) {
            badCharHeuristic[pattern[j]] = j;
        }

        if (patLen == 0) {
            for (int j = 0; j <= textLen; ++j) {
                positions.push_back(j);
            }
            return positions;
        }

        while (i <= textLen - patLen) {
            int mismatchIndex = mismatchInText(i);
            if (mismatchIndex == -1) {
                positions.push_back(i);
                i += patLen;
            } else {
                char mismatchChar = text[mismatchIndex];
                int matchIndex = -1;
                auto it = badCharHeuristic.find(mismatchChar);
                if (it != badCharHeuristic.end()) {
                    matchIndex = it->second;
                }
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