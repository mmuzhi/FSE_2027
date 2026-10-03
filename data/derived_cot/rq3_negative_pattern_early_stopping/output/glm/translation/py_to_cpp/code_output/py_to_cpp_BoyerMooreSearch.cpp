#include <string>
#include <vector>

class BoyerMooreSearch {
public:
    std::string text;
    std::string pattern;
    int textLen;
    int patLen;

    BoyerMooreSearch(std::string text, std::string pattern)
        : text(text), pattern(pattern), textLen(this->text.length()), patLen(this->pattern.length()) {}

    int match_in_pattern(char c) const {
        for (int i = patLen - 1; i >= 0; --i) {
            if (pattern[i] == c) {
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

    std::vector<int> bad_character_heuristic() {
        std::vector<int> positions;
        for (int i_counter = 0; i_counter < textLen - patLen + 1; ++i_counter) {
            int i = i_counter;
            int mismatch_index = mismatch_in_text(i);
            if (mismatch_index == -1) {
                positions.push_back(i);
            } else {
                int match_index = match_in_pattern(text[mismatch_index]);
                i = mismatch_index - match_index;
            }
        }
        return positions;
    }
};