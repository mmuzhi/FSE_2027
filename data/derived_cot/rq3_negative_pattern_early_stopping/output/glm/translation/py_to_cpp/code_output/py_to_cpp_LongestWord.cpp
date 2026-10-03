#include <string>
#include <vector>
#include <algorithm>
#include <cctype>

class LongestWord {
private:
    std::vector<std::string> word_list;

public:
    LongestWord() {}

    void add_word(const std::string& word) {
        word_list.push_back(word);
    }

    std::string find_longest_word(std::string sentence) {
        std::string longest_word = "";
        
        for (char& c : sentence) {
            c = std::tolower(static_cast<unsigned char>(c));
        }
        
        static const std::string punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";
        std::string cleaned;
        for (char c : sentence) {
            if (punctuation.find(c) == std::string::npos) {
                cleaned += c;
            }
        }
        
        std::vector<std::string> words;
        std::string current_word;
        for (size_t i = 0; i < cleaned.length(); ++i) {
            if (cleaned[i] == ' ') {
                words.push_back(current_word);
                current_word.clear();
            } else {
                current_word += cleaned[i];
            }
        }
        words.push_back(current_word);
        
        for (const std::string& word : words) {
            if (std::find(word_list.begin(), word_list.end(), word) != word_list.end() && word.length() > longest_word.length()) {
                longest_word = word;
            }
        }
        
        return longest_word;
    }
};