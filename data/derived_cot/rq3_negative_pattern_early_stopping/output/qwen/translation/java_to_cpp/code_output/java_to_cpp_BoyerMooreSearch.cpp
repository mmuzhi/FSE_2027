#include <vector>
#include <unordered_map>
#include <string>
#include <algorithm>

class BoyerMooreSearch {
private:
    std::string text;
    std::string pattern;
    int textLen;
    int patLen;

public:
    BoyerMooreSearch(const std::string& text, const std::string& pattern)
        : text(text), pattern(pattern), textLen(text.length()), patLen(pattern.length()) {}

    int matchInPattern(char ch) {
        for (int i = patLen - 1; i >= 0; i--) {
            if (pattern[i] == ch) {
                return i;
            }
        }
        return -1;
    }

    int mismatchInText(int currentPos) {
        for (int i = patLen - 1; i >= 0; i--) {
            if (pattern[i] != text[currentPos + i]) {
                return currentPos + i;
            }
        }
        return -1;
    }

    std::vector<int> badCharacterHeuristic() {
        std::vector<int> positions;
        if (patLen == 0) {
            for (int j = 0; j <= textLen; j++) {
                positions.push_back(j);
            }
            return positions;
        }

        std::unordered_map<char, int> badCharHeuristic;
        for (int j = 0; j < patLen; j++) {
            badCharHeuristic[pattern[j]] = j;
        }

        int i = 0;
        while (i <= textLen - patLen) {
            int mismatchIndex = mismatchInText(i);
            if (mismatchIndex == -1) {
                positions.push_back(i);
                i += patLen;
            } else {
                char mismatchChar = text[mismatchIndex];
                auto it = badCharHeuristic.find(mismatchChar);
                int matchIndex = -1;
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