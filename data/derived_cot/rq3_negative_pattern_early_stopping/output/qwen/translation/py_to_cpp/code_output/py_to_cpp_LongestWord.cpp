#include <vector>
#include <string>
#include <algorithm>
#include <sstream>
#include <cctype>

class LongestWord {
private:
    std::vector<std::string> word_list;

public:
    void add_word(const std::string& word) {
        word_list.push_back(word);
    }

    std::string find_longest_word(std::string sentence) {
        // Convert the sentence to lowercase
        for (char &c : sentence) {
            c = std::tolower(c);
        }

        // Define the punctuation string
        std::string punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";
        // Remove each punctuation character
        for (char c : punctuation) {
            sentence.erase(std::remove(sentence.begin(), sentence.end(), c), sentence.end());
        }

        // Split the sentence by spaces
        std::istringstream iss(sentence);
        std::string word;
        std::vector<std::string> words;
        while (iss >> word) {
            words.push_back(word);
        }

        // Find the longest word in the list that is in the word_list
        std::string longest_word = "";
        for (const std::string& w : words) {
            // Check if w is in the word_list
            auto it = std::find(word_list.begin(), word_list.end(), w);
            if (it != word_list.end()) {
                if (w.length() > longest_word.length()) {
                    longest_word = w;
                }
            }
        }

        return longest_word;
    }
};