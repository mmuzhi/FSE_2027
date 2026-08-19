#include <string>
#include <vector>
#include <algorithm>
#include <cctype>

class LongestWord {
public:
    LongestWord() {}

    void add_word(const std::string& word) {
        word_list.push_back(word);
    }

    std::string find_longest_word(std::string sentence) {
        std::string longest_word = "";

        // sentence.lower() -- ASCII semantics (A-Z -> a-z)
        for (char& c : sentence) {
            c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
        }

        // re.sub('[%s]' % re.escape(string.punctuation), '', sentence)
        static const std::string punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";
        sentence.erase(
            std::remove_if(sentence.begin(), sentence.end(),
                           [&](char c) { return punctuation.find(c) != std::string::npos; }),
            sentence.end());

        // re.split(' ', sentence) -- literal single-space split,
        // consecutive/leading/trailing spaces yield empty tokens
        std::vector<std::string> words;
        std::string current;
        for (char c : sentence) {
            if (c == ' ') {
                words.push_back(current);
                current.clear();
            } else {
                current += c;
            }
        }
        words.push_back(current);

        // membership check is exact (case-sensitive) against word_list;
        // strictly greater length keeps the first longest match
        for (const std::string& word : words) {
            bool in_list = std::find(word_list.begin(), word_list.end(), word) != word_list.end();
            if (in_list && word.size() > longest_word.size()) {
                longest_word = word;
            }
        }
        return longest_word;
    }

private:
    std::vector<std::string> word_list;
};