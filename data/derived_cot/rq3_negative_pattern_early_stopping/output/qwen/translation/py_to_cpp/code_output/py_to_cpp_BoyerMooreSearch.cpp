#include <vector>
#include <string>
#include <algorithm>

class BoyerMooreSearch {
private:
    std::string text;
    std::string pattern;
    int textLen;
    int patLen;

    // Helper function to find the rightmost occurrence of a character in the pattern
    int match_in_pattern(char c) {
        for (int i = patLen - 1; i >= 0; i--) {
            if (pattern[i] == c) {
                return i;
            }
        }
        return -1;
    }

    // Helper function to find the first mismatch position in the text starting at currentPos
    int mismatch_in_text(int currentPos) {
        for (int i = patLen - 1; i >= 0; i--) {
            if (pattern[i] != text[currentPos + i]) {
                return currentPos + i;
            }
        }
        return -1;
    }

public:
    // Constructor
    BoyerMooreSearch(const std::string& text, const std::string& pattern) {
        this->text = text;
        this->pattern = pattern;
        this->textLen = text.length();
        this->patLen = pattern.length();
    }

    // Main function to find all occurrences using the bad character heuristic
    std::vector<int> bad_character_heuristic() {
        std::vector<int> positions;
        for (int i = 0; i <= textLen - patLen; i++) {
            int mismatch_index = mismatch_in_text(i);
            if (mismatch_index == -1) {
                // No mismatch, so we found a match
                positions.push_back(i);
            } else {
                // There was a mismatch, so we use the bad character heuristic to jump
                int match_index = match_in_pattern(text[mismatch_index]);
                // The step to jump is (mismatch_index - match_index)
                i = mismatch_index - match_index;
            }
        }
        return positions;
    }
};