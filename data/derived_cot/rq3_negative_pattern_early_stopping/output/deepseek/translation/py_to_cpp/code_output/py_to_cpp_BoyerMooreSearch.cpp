#include <string>
#include <vector>

class BoyerMooreSearch {
private:
    std::string text;
    std::string pattern;
    int textLen;
    int patLen;

public:
    BoyerMooreSearch(const std::string& t, const std::string& p)
        : text(t), pattern(p), textLen(t.size()), patLen(p.size()) {}

    int match_in_pattern(char ch) const {
        for (int i = patLen - 1; i >= 0; --i) {
            if (ch == pattern[i]) {
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
        int i = 0;
        while (i <= textLen - patLen) {
            int mismatch_index = mismatch_in_text(i);
            if (mismatch_index == -1) {
                positions.push_back(i);
                ++i;
            } else {
                int match_index = match_in_pattern(text[mismatch_index]);
                int shift = mismatch_index - match_index;
                i += shift;
            }
        }
        return positions;
    }
};