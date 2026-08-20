// The class allows to split sentences, count words in a sentence, and process
// a text file to find the maximum word count.

#include <cstddef>
#include <string>
#include <vector>

class SplitSentence {
public:
    // Split a string into a list of sentences. Sentences end with . or ? followed
    // by whitespace. Note that abbreviations such as "Mr." or "e.g." also end
    // with . but are not treated as sentence ends.
    // Equivalent to: re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', s)
    std::vector<std::string> split_sentences(const std::string& sentences_string) const {
        const std::string& s = sentences_string;
        const std::size_t n = s.size();
        std::vector<std::string> sentences;
        std::size_t start = 0;

        for (std::size_t i = 0; i < n; ++i) {
            // The pattern matches a single whitespace character...
            if (!is_space(s[i])) {
                continue;
            }
            // ...that is preceded by '.' or '?'   ((?<=\.|\?))
            if (i == 0 || (s[i - 1] != '.' && s[i - 1] != '?')) {
                continue;
            }
            // ...and not preceded by a "\w\.\w." sequence   ((?<!\w\.\w.)),
            // e.g. "e.g." or "U.S." ('.' matches any char but '\n')
            if (i >= 4 && is_word(s[i - 4]) && s[i - 3] == '.' &&
                is_word(s[i - 2]) && s[i - 1] != '\n') {
                continue;
            }
            // ...and not preceded by an "[A-Z][a-z]\." sequence
            // ((?<![A-Z][a-z]\.)), e.g. "Mr."
            if (i >= 3 && is_upper(s[i - 3]) && is_lower(s[i - 2]) &&
                s[i - 1] == '.') {
                continue;
            }
            // Split point found at i; the matched whitespace is dropped.
            sentences.push_back(s.substr(start, i - start));
            start = i + 1;
        }
        sentences.push_back(s.substr(start));
        return sentences;
    }

    // Count the number of words in a sentence. Words are separated by spaces;
    // punctuation marks and numbers are not counted as words.
    // Equivalent to: len(re.sub(r'[^a-zA-Z\s]', '', s).split())
    int count_words(const std::string& sentence) const {
        int count = 0;
        bool in_word = false;
        for (const char c : sentence) {
            if (is_alpha(c)) {
                if (!in_word) {
                    ++count;
                    in_word = true;
                }
            } else if (is_space(c)) {
                in_word = false;
            }
            // Any other character is stripped by the substitution: it neither
            // starts nor terminates a word.
        }
        return count;
    }

    // Given a text, return the number of words in the longest sentence.
    int process_text_file(const std::string& sentences_string) const {
        const std::vector<std::string> sentences = split_sentences(sentences_string);
        int max_count = 0;
        for (const std::string& sentence : sentences) {
            const int count = count_words(sentence);
            if (count > max_count) {
                max_count = count;
            }
        }
        return max_count;
    }

private:
    // ASCII '\s': [ \t\n\r\f\v]
    static bool is_space(char c) {
        return c == ' ' || c == '\t' || c == '\n' || c == '\r' ||
               c == '\f' || c == '\v';
    }
    // ASCII '\w': [A-Za-z0-9_]
    static bool is_word(char c) {
        return is_alpha(c) || (c >= '0' && c <= '9') || c == '_';
    }
    static bool is_alpha(char c) {
        return is_upper(c) || is_lower(c);
    }
    static bool is_upper(char c) {
        return c >= 'A' && c <= 'Z';
    }
    static bool is_lower(char c) {
        return c >= 'a' && c <= 'z';
    }
};