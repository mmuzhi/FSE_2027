#include <string>
#include <vector>
#include <cctype>

class SplitSentence {
public:
    std::vector<std::string> split_sentences(const std::string& sentences_string) {
        std::vector<std::string> result;
        std::string current;

        for (size_t i = 0; i < sentences_string.size(); ++i) {
            char c = sentences_string[i];

            bool is_whitespace = c == ' ' || c == '\t' || c == '\n' || c == '\r' || c == '\f' || c == '\v';

            if (is_whitespace && i > 0 && (sentences_string[i - 1] == '.' || sentences_string[i - 1] == '?')) {
                bool abbrev1 = false;
                if (i >= 3) {
                    char c3 = sentences_string[i - 3];
                    char c2 = sentences_string[i - 2];
                    char c1 = sentences_string[i - 1];
                    if (c3 >= 'A' && c3 <= 'Z' && c2 >= 'a' && c2 <= 'z' && c1 == '.') {
                        abbrev1 = true;
                    }
                }

                bool abbrev2 = false;
                if (i >= 4) {
                    char c4 = sentences_string[i - 4];
                    char c3 = sentences_string[i - 3];
                    char c2 = sentences_string[i - 2];
                    char c1 = sentences_string[i - 1];
                    if (std::isalnum(static_cast<unsigned char>(c4)) && c3 == '.' &&
                        std::isalnum(static_cast<unsigned char>(c2)) && c1 == '.') {
                        abbrev2 = true;
                    }
                }

                if (!abbrev1 && !abbrev2) {
                    result.push_back(current);
                    current.clear();
                    continue;
                }
            }

            current += c;
        }

        if (!current.empty()) {
            result.push_back(current);
        }

        return result;
    }

    int count_words(const std::string& sentence) {
        std::string cleaned;
        for (char c : sentence) {
            if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == ' ' || c == '\t' || c == '\n' || c == '\r') {
                cleaned += c;
            }
        }

        int count = 0;
        bool in_word = false;
        for (char c : cleaned) {
            if (c == ' ' || c == '\t' || c == '\n' || c == '\r') {
                in_word = false;
            } else {
                if (!in_word) {
                    count++;
                    in_word = true;
                }
            }
        }

        return count;
    }

    int process_text_file(const std::string& sentences_string) {
        std::vector<std::string> sentences = split_sentences(sentences_string);
        int max_count = 0;
        for (const auto& sentence : sentences) {
            int count = count_words(sentence);
            if (count > max_count) {
                max_count = count;
            }
        }
        return max_count;
    }
};