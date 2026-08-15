#include <string>
#include <vector>
#include <algorithm>
#include <cctype>

class LongestWord {
public:
    void add_word(const std::string& word) {
        word_list.push_back(word);
    }

    std::string find_longest_word(const std::string& sentence) {
        std::string processed = sentence;
        std::transform(processed.begin(), processed.end(), processed.begin(),
                       [](unsigned char c) { return static_cast<char>(std::tolower(c)); });

        const std::string punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";
        processed.erase(
            std::remove_if(processed.begin(), processed.end(),
                           [&](char c) {
                               return punctuation.find(c) != std::string::npos;
                           }),
            processed.end());

        std::vector<std::string> words;
        std::string current;
        for (char c : processed) {
            if (c == ' ') {
                words.push_back(current);
                current.clear();
            } else {
                current.push_back(c);
            }
        }
        words.push_back(current);

        std::string longest_word;
        for (const std::string& word : words) {
            if (std::find(word_list.begin(), word_list.end(), word) != word_list.end()) {
                if (word.size() > longest_word.size()) {
                    longest_word = word;
                }
            }
        }
        return longest_word;
    }

private:
    std::vector<std::string> word_list;
};