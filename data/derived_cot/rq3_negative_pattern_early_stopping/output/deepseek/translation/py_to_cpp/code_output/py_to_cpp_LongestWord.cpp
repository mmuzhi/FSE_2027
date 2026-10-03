#include <string>
#include <vector>
#include <algorithm>
#include <cctype>
#include <sstream>
#include <regex>

class LongestWord {
public:
    LongestWord() {}

    void add_word(const std::string& word) {
        word_list.push_back(word);
    }

    std::string find_longest_word(const std::string& sentence) {
        std::string longest_word = "";

        // Convert sentence to lowercase
        std::string lower_sentence = sentence;
        std::transform(lower_sentence.begin(), lower_sentence.end(), lower_sentence.begin(),
                       [](unsigned char c) { return std::tolower(c); });

        // Remove punctuation
        std::string clean_sentence;
        std::regex punct_re("[[:punct:]]");
        clean_sentence = std::regex_replace(lower_sentence, punct_re, "");

        // Split by spaces
        std::vector<std::string> words;
        std::istringstream stream(clean_sentence);
        std::string word;
        while (stream >> word) {
            words.push_back(word);
        }

        // Find longest word that is in word_list
        for (const auto& w : words) {
            if (std::find(word_list.begin(), word_list.end(), w) != word_list.end()) {
                if (w.length() > longest_word.length()) {
                    longest_word = w;
                }
            }
        }

        return longest_word;
    }

private:
    std::vector<std::string> word_list;
};