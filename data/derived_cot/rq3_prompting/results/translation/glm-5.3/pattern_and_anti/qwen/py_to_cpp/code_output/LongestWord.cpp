#include <string>
#include <vector>
#include <algorithm>
#include <cctype>

class LongestWord {
public:
    std::vector<std::string> word_list;

    LongestWord() : word_list() {}

    void add_word(const std::string& word) {
        word_list.push_back(word);
    }

    std::string find_longest_word(std::string sentence) {
        std::string longest_word = "";

        // sentence.lower()
        for (char& c : sentence) {
            c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
        }

        // remove Python string.punctuation characters
        static const std::string punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";
        std::string cleaned;
        for (char c : sentence) {
            if (punctuation.find(c) == std::string::npos) {
                cleaned += c;
            }
        }

        // re.split(' ', sentence): split on single spaces (empty tokens preserved)
        std::vector<std::string> words;
        std::string::size_type start = 0;
        std::string::size_type pos;
        while ((pos = cleaned.find(' ', start)) != std::string::npos) {
            words.push_back(cleaned.substr(start, pos - start));
            start = pos + 1;
        }
        words.push_back(cleaned.substr(start));

        for (const std::string& word : words) {
            bool in_list = std::find(word_list.begin(), word_list.end(), word) != word_list.end();
            if (in_list && word.length() > longest_word.length()) {
                longest_word = word;
            }
        }
        return longest_word;
    }
};