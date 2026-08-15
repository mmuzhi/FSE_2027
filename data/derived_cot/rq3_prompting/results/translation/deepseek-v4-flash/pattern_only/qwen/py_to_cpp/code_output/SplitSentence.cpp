#include <string>
#include <vector>

namespace {

bool is_space(char c) {
    return c == ' ' || c == '\t' || c == '\n' || c == '\r' || c == '\f' || c == '\v';
}

bool is_word(char c) {
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') ||
           (c >= '0' && c <= '9') || c == '_';
}

bool is_upper(char c) {
    return c >= 'A' && c <= 'Z';
}

bool is_lower(char c) {
    return c >= 'a' && c <= 'z';
}

} // namespace

class SplitSentence {
public:
    std::vector<std::string> split_sentences(const std::string& sentences_string) const;
    int count_words(const std::string& sentence) const;
    int process_text_file(const std::string& sentences_string) const;
};

std::vector<std::string> SplitSentence::split_sentences(const std::string& s) const {
    std::vector<std::string> sentences;
    if (s.empty()) {
        sentences.push_back("");
        return sentences;
    }

    std::string current;
    for (size_t i = 0; i < s.size(); ++i) {
        char c = s[i];

        if (is_space(c) && i > 0 && (s[i - 1] == '.' || s[i - 1] == '?')) {
            bool negative1 = false;
            if (i >= 4) {
                if (is_word(s[i - 4]) && s[i - 3] == '.' && is_word(s[i - 2])) {
                    negative1 = true;
                }
            }

            bool negative2 = false;
            if (i >= 3) {
                if (is_upper(s[i - 3]) && is_lower(s[i - 2]) && s[i - 1] == '.') {
                    negative2 = true;
                }
            }

            if (!negative1 && !negative2) {
                sentences.push_back(current);
                current.clear();
                continue;
            }
        }

        current.push_back(c);
    }

    sentences.push_back(current);
    return sentences;
}

int SplitSentence::count_words(const std::string& sentence) const {
    std::string filtered;
    for (char c : sentence) {
        if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || is_space(c)) {
            filtered.push_back(c);
        }
    }

    int count = 0;
    bool in_word = false;
    for (char c : filtered) {
        if (is_space(c)) {
            in_word = false;
        } else if (!in_word) {
            ++count;
            in_word = true;
        }
    }

    return count;
}

int SplitSentence::process_text_file(const std::string& sentences_string) const {
    std::vector<std::string> sentences = split_sentences(sentences_string);
    int max_count = 0;
    for (const std::string& sentence : sentences) {
        int count = count_words(sentence);
        if (count > max_count) {
            max_count = count;
        }
    }
    return max_count;
}