#include <string>
#include <vector>

class BoyerMooreSearch {
public:
    BoyerMooreSearch(const std::string& text, const std::string& pattern)
        : text(text), pattern(pattern),
          textLen(static_cast<int>(text.size())),
          patLen(static_cast<int>(pattern.size())) {}

    // Finds the rightmost occurrence of a character in the pattern.
    int match_in_pattern(char ch) const {
        for (int i = patLen - 1; i >= 0; --i) {
            if (ch == pattern[i]) {
                return i;
            }
        }
        return -1;
    }

    // Determines the position of the first mismatch between the pattern and the text.
    int mismatch_in_text(int currentPos) const {
        for (int i = patLen - 1; i >= 0; --i) {
            if (pattern[i] != text[currentPos + i]) {
                return currentPos + i;
            }
        }
        return -1;
    }

    // Finds all occurrences of the pattern in the text.
    std::vector<int> bad_character_heuristic() const {
        std::vector<int> positions;
        for (int i = 0; i < textLen - patLen + 1; ++i) {
            int mismatch_index = mismatch_in_text(i);
            if (mismatch_index == -1) {
                positions.push_back(i);
            } else {
                int match_index = match_in_pattern(text[mismatch_index]);
                // In the Python original, `i = mismatch_index - match_index` is
                // dead code: reassigning the loop variable of a `for ... in
                // range(...)` loop does not affect iteration. It is therefore
                // omitted here so the C++ loop advances identically.
                (void)match_index;
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