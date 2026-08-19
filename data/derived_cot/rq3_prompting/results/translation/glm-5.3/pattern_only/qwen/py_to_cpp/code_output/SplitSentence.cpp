#include <string>
#include <vector>

class SplitSentence {
public:
    // Split a string into a list of sentences. Sentences end with . or ? followed
    // by a space. Note that "Mr." also ends with . but is not a sentence.
    // Equivalent to Python: re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', s)
    std::vector<std::string> split_sentences(const std::string& sentences_string) const {
        std::vector<std::string> sentences;
        std::size_t start = 0;
        for (std::size_t i = 0; i < sentences_string.size(); ++i) {
            if (!is_space(sentences_string[i]))
                continue;
            if (i == 0)
                continue; // (?<=\.|\?) requires a preceding character
            char prev = sentences_string[i - 1];
            if (prev != '.' && prev != '?')
                continue;
            // Negative lookbehind (?<!\w\.\w.): the 4 chars before must not match \w . \w .
            if (i >= 4) {
                if (is_word(sentences_string[i - 4]) && sentences_string[i - 3] == '.' &&
                    is_word(sentences_string[i - 2]) && prev != '\n')
                    continue;
            }
            // Negative lookbehind (?<![A-Z][a-z]\.): the 3 chars before must not match [A-Z][a-z]\.
            if (i >= 3) {
                if (sentences_string[i - 3] >= 'A' && sentences_string[i - 3] <= 'Z' &&
                    sentences_string[i - 2] >= 'a' && sentences_string[i - 2] <= 'z' &&
                    prev == '.')
                    continue;
            }
            // Split here: consume exactly one whitespace character
            sentences.push_back(sentences_string.substr(start, i - start));
            start = i + 1;
        }
        sentences.push_back(sentences_string.substr(start));
        return sentences;
    }

    // Count the number of words in a sentence. Words are separated by spaces;
    // punctuation marks and numbers are not counted as words.
    // Equivalent to Python: re.sub(r'[^a-zA-Z\s]', '', s).split() length
    int count_words(const std::string& sentence) const {
        // re.sub: remove every char that is neither [a-zA-Z] nor whitespace
        std::string cleaned;
        for (char c : sentence) {
            if (is_letter(c) || is_space(c))
                cleaned.push_back(c);
        }
        // str.split(): count whitespace-separated tokens
        int count = 0;
        bool in_word = false;
        for (char c : cleaned) {
            if (is_space(c)) {
                in_word = false;
            } else if (!in_word) {
                ++count;
                in_word = true;
            }
        }
        return count;
    }

    // Return the number of words in the longest sentence.
    int process_text_file(const std::string& sentences_string) const {
        std::vector<std::string> sentences = split_sentences(sentences_string);
        int max_count = 0;
        for (const std::string& sentence : sentences) {
            int count = count_words(sentence);
            if (count > max_count)
                max_count = count;
        }
        return max_count;
    }

private:
    static bool is_space(char c) { // \s (ASCII)
        return c == ' ' || c == '\t' || c == '\n' ||
               c == '\v' || c == '\f' || c == '\r';
    }
    static bool is_letter(char c) { // [a-zA-Z]
        return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z');
    }
    static bool is_word(char c) { // \w (ASCII approximation)
        return is_letter(c) || (c >= '0' && c <= '9') || c == '_';
    }
};