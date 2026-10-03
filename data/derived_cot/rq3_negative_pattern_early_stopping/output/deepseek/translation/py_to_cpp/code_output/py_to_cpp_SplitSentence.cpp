#include <string>
#include <vector>
#include <sstream>
#include <cctype>

class SplitSentence {
public:
    std::vector<std::string> split_sentences(const std::string& sentences_string) {
        std::vector<std::string> result;
        size_t start = 0;
        size_t len = sentences_string.length();
        for (size_t i = 0; i < len; ++i) {
            char c = sentences_string[i];
            if ((c == '.' || c == '?') && i + 1 < len && std::isspace(static_cast<unsigned char>(sentences_string[i+1]))) {
                bool forbid = false;
                if (c == '.') {
                    forbid = is_forbidden(sentences_string, i);
                }
                if (!forbid) {
                    result.push_back(sentences_string.substr(start, i - start + 1));
                    start = i + 2;
                }
            }
        }
        if (start < len) {
            result.push_back(sentences_string.substr(start));
        } else if (result.empty() && len == 0) {
            result.push_back("");
        }
        return result;
    }

    int count_words(const std::string& sentence) {
        std::string cleaned;
        cleaned.reserve(sentence.size());
        for (unsigned char ch : sentence) {
            if (std::isalpha(ch) || std::isspace(ch)) {
                cleaned += static_cast<char>(ch);
            }
        }
        std::istringstream stream(cleaned);
        std::string word;
        int count = 0;
        while (stream >> word) {
            ++count;
        }
        return count;
    }

    int process_text_file(const std::string& sentences_string) {
        std::vector<std::string> sentences = split_sentences(sentences_string);
        int max_count = 0;
        for (const auto& sentence : sentences) {
            int cnt = count_words(sentence);
            if (cnt > max_count) {
                max_count = cnt;
            }
        }
        return max_count;
    }

private:
    bool is_forbidden(const std::string& s, size_t dot_pos) {
        if (dot_pos >= 2) {
            if (std::isupper(static_cast<unsigned char>(s[dot_pos-2])) &&
                std::islower(static_cast<unsigned char>(s[dot_pos-1])) &&
                s[dot_pos] == '.') {
                return true;
            }
        }
        if (dot_pos >= 3) {
            if (is_word_char(s[dot_pos-3]) &&
                s[dot_pos-2] == '.' &&
                is_word_char(s[dot_pos-1]) &&
                s[dot_pos] == '.') {
                return true;
            }
        }
        return false;
    }

    bool is_word_char(char ch) {
        return std::isalnum(static_cast<unsigned char>(ch)) || ch == '_';
    }
};