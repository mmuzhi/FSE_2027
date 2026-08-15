#include <string>
#include <vector>

class BoyerMooreSearch {
private:
    std::string text;
    std::string pattern;
    int textLen;
    int patLen;

public:
    BoyerMooreSearch(const std::string& text, const std::string& pattern)
        : text(text), pattern(pattern), textLen(static_cast<int>(text.size())), patLen(static_cast<int>(pattern.size())) {}

    int match_in_pattern(char c) const {
        for (int i = patLen - 1; i >= 0; --i) {
            if (c == pattern[i]) {
                return i;
            }
        }
        return -1;
    }

    int mismatch_in_text(int currentPos) const {
        for (int i = patLen - 1; i >= 0; --i) {
            if (pattern[i] != text[currentPos + i]) {
                return currentPos + i;
            }
        }
        return -1;
    }

    std::vector<int> bad_character_heuristic() const {
        std::vector<int> positions;
        for (int i = 0; i < textLen - patLen + 1; ++i) {
            int mismatch_index = mismatch_in_text(i);
            if (mismatch_index == -1) {
                positions.push_back(i);
            } else {
                int match_index = match_in_pattern(text[mismatch_index]);
                // In the original Python, `i = mismatch_index - match_index`
                // has no effect on the for-loop iteration, so it is intentionally omitted.
            }
        }
        return positions;
    }
};