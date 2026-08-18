#include <cctype>
#include <string>
#include <vector>

class SplitSentence {
private:
    // Equivalent of Python's \s (ASCII whitespace set)
    static bool is_space_char(char c) {
        return c == ' ' || c == '\t' || c == '\n' || c == '\v' || c == '\f' || c == '\r';
    }

    // Equivalent of Python's \w (ASCII word character)
    static bool is_word_char(char c) {
        unsigned char u = static_cast<unsigned char>(c);
        return std::isalnum(u) != 0 || c == '_';
    }

public:
    // Split a string into a list of sentences. Sentences end with . or ? followed by
    // a space. Abbreviations such as "Mr." also end with . but are not sentences.
    // Reimplements re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', s):
    // split on a single whitespace char whose preceding char is '.' or '?',
    // unless the text before it matches \w\.\w. or [A-Z][a-z]\.
    std::vector<std::string> split_sentences(const std::string& sentences_string) const {
        std::vector<std::string> sentences;
        std::string current;
        const std::size_t n = sentences_string.size();
        for (std::size_t i = 0; i < n; ++i) {
            const char c = sentences_string[i];
            if (is_space_char(c) && i > 0) {
                const char prev = sentences_string[i - 1];
                if (prev == '.' || prev == '?') {
                    // Negative lookbehind: \w\.\w. (the trailing '.' matches any
                    // non-newline char; here it is always the '.'/'?' at prev)
                    bool abbr1 = false;
                    if (i >= 4) {
                        const char a = sentences_string[i - 4];
                        const char b = sentences_string[i - 3];
                        const char d = sentences_string[i - 2];
                        if (is_word_char(a) && b == '.' && is_word_char(d)) {
                            abbr1 = true;
                        }
                    }
                    // Negative lookbehind: [A-Z][a-z]\. (e.g., "Mr.")
                    bool abbr2 = false;
                    if (i >= 3) {
                        const char a = sentences_string[i - 3];
                        const char b = sentences_string[i - 2];
                        if (std::isupper(static_cast<unsigned char>(a)) != 0 &&
                            std::islower(static_cast<unsigned char>(b)) != 0 &&
                            prev == '.') {
                            abbr2 = true;
                        }
                    }
                    if (!abbr1 && !abbr2) {
                        sentences.push_back(current);
                        current.clear();
                        continue; // this whitespace char is consumed by the split
                    }
                }
            }
            current += c;
        }
        sentences.push_back(current); // re.split always emits the trailing piece
        return sentences;
    }

    // Count the number of words in a sentence. Words are separated by spaces;
    // punctuation marks and numbers are not counted as words.
    // Equivalent of: re.sub(r'[^a-zA-Z\s]', '', sentence).split() -> len
    int count_words(const std::string& sentence) const {
        std::string filtered;
        for (char c : sentence) {
            if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || is_space_char(c)) {
                filtered += c;
            }
        }
        int words = 0;
        bool in_word = false;
        for (char c : filtered) {
            if (is_space_char(c)) {
                in_word = false;
            } else {
                if (!in_word) ++words;
                in_word = true;
            }
        }
        return words;
    }

    // Given a text, return the number of words in the longest sentence.
    int process_text_file(const std::string& sentences_string) const {
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
};