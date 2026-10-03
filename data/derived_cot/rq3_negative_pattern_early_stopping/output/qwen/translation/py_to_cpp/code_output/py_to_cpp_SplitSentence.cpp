#include <regex>
#include <vector>
#include <string>
#include <cctype>
#include <algorithm>

class SplitSentence {
public:
    std::vector<std::string> split_sentences(const std::string& sentences_string) {
        // The regex pattern from Python: (?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s
        // We'll use the same pattern in C++.
        std::regex pattern(R"((?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s)");
        // We want to split the string by the pattern, but note that the pattern includes a space at the end.
        // We can use the regex to split by replacing the delimiters with a null character and then splitting by nulls?
        // Alternatively, we can use the regex_token_iterator.

        // Let's use the regex_token_iterator with the delimiter being the pattern, but note that the pattern is a space that is preceded by a dot or question mark and not part of an abbreviation.

        // However, the standard library doesn't have a split function, so we can use:
        std::sregex_token_iterator iter(sentences_string.begin(), sentences_string.end(), pattern, 0);
        std::sregex_token_iterator end;

        std::vector<std::string> sentences;
        for (std::string sentence = *iter++; iter != end; ++iter) {
            sentences.push_back(sentence);
        }

        return sentences;
    }

    int count_words(const std::string& sentence) {
        // Remove all non-alphabetic characters (except spaces) and then split by spaces.
        std::string cleaned;
        for (char c : sentence) {
            if (std::isalpha(c) || std::isspace(c)) {
                cleaned.push_back(c);
            }
        }
        // Now split the cleaned string by spaces.
        std::istringstream iss(cleaned);
        std::string word;
        int count = 0;
        while (iss >> word) {
            count++;
        }
        return count;
    }

    int process_text_file(const std::string& sentences_string) {
        std::vector<std::string> sentences = this->split_sentences(sentences_string);
        int max_count = 0;
        for (const auto& sentence : sentences) {
            int count = this->count_words(sentence);
            if (count > max_count) {
                max_count = count;
            }
        }
        return max_count;
    }
};