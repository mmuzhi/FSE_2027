#include <string>
#include <vector>
#include <utility>

class BoyerMooreSearch {
public:
    BoyerMooreSearch(std::string text, std::string pattern)
        : text(std::move(text)), pattern(std::move(pattern)),
          textLen(static_cast<int>(this->text.size())),
          patLen(static_cast<int>(this->pattern.size())) {}

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
                // In Python, rebinding the loop variable `i` here has no
                // effect on the range iteration, so this value is unused.
                (void)(mismatch_index - match_index);
            }
        }
        return positions;
    }

private:
    std::string text;
    std::string pattern;
    int textLen;
    int patLen;
};