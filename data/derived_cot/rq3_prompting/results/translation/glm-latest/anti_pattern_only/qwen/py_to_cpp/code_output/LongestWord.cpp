#include <algorithm>
#include <cctype>
#include <string>
#include <vector>

// This is a class that allows to add words to a list and find the longest
// word in a given sentence by comparing the words with the ones in the word list.

class LongestWord {
public:
    // Public to mirror the accessible Python attribute `self.word_list`.
    std::vector<std::string> word_list;

    LongestWord() = default;

    // Append the input word into word_list.
    void add_word(const std::string& word) {
        word_list.push_back(word);
    }

    // Lower-case the sentence, remove punctuation marks, and split it on single
    // spaces. Find the longest split word that is present in word_list
    // (comparison is case-sensitive). Returns "" if no such word exists.
    std::string find_longest_word(const std::string& sentence) const {
        std::string longest_word;

        // sentence.lower()
        std::string lowered;
        lowered.reserve(sentence.size());
        for (unsigned char c : sentence) {
            lowered.push_back(static_cast<char>(std::tolower(c)));
        }

        // Remove every character found in Python's string.punctuation:
        // !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        static const std::string punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";
        std::string cleaned;
        cleaned.reserve(lowered.size());
        for (char c : lowered) {
            if (punctuation.find(c) == std::string::npos) {
                cleaned.push_back(c);
            }
        }

        // re.split(' ', sentence): split on every single space,
        // keeping empty fields for consecutive/leading/trailing spaces.
        std::vector<std::string> words;
        std::string current;
        for (char c : cleaned) {
            if (c == ' ') {
                words.push_back(current);
                current.clear();
            } else {
                current.push_back(c);
            }
        }
        words.push_back(current);

        // Find the longest word that is in word_list (strict case-sensitive match).
        for (const std::string& word : words) {
            bool in_list =
                std::find(word_list.begin(), word_list.end(), word) != word_list.end();
            if (in_list && word.size() > longest_word.size()) {
                longest_word = word;
            }
        }
        return longest_word;
    }
};