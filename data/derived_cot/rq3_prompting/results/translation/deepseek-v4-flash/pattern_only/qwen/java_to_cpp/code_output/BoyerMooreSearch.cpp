#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>

class BoyerMooreSearch {
private:
    std::u16string text;
    std::u16string pattern;
    int textLen;
    int patLen;

public:
    BoyerMooreSearch(const std::u16string& text, const std::u16string& pattern)
        : text(text), pattern(pattern),
          textLen(static_cast<int>(text.length())),
          patLen(static_cast<int>(pattern.length())) {}

    int matchInPattern(char16_t ch) const {
        std::size_t pos = pattern.find_last_of(ch);
        return pos == std::u16string::npos ? -1 : static_cast<int>(pos);
    }

    int mismatchInText(int currentPos) const {
        for (int i = patLen - 1; i >= 0; --i) {
            if (pattern.at(i) != text.at(currentPos + i)) {
                return currentPos + i;
            }
        }
        return -1;
    }

    std::vector<int> badCharacterHeuristic() const {
        std::vector<int> positions;
        int i = 0;

        std::unordered_map<char16_t, int> badCharHeuristic;
        for (int j = 0; j < patLen; ++j) {
            badCharHeuristic[pattern.at(j)] = j;
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
                char16_t mismatchChar = text.at(mismatchIndex);
                auto it = badCharHeuristic.find(mismatchChar);
                int matchIndex = (it != badCharHeuristic.end()) ? it->second : -1;
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