#include <algorithm>
#include <cctype>
#include <iostream>
#include <string>
#include <vector>

class LongestWord {
private:
    std::vector<std::string> wordList;

public:
    LongestWord() {}

    void addWord(const std::string& word) {
        wordList.push_back(word);
    }

    std::string findLongestWord(std::string sentence) {
        std::string longestWord = "";
        std::transform(sentence.begin(), sentence.end(), sentence.begin(), [](unsigned char c){ return std::tolower(c); });
        
        std::string punct = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";
        sentence.erase(std::remove_if(sentence.begin(), sentence.end(), [&punct](char c) {
            return punct.find(c) != std::string::npos;
        }), sentence.end());

        std::vector<std::string> words;
        bool found = false;
        std::string current;
        for (size_t i = 0; i < sentence.length(); ++i) {
            if (sentence[i] == ' ') {
                found = true;
                words.push_back(current);
                current.clear();
            } else {
                current += sentence[i];
            }
        }
        words.push_back(current);
        if (found) {
            while (!words.empty() && words.back().empty()) {
                words.pop_back();
            }
        }

        for (const std::string& w : words) {
            if (std::find(wordList.begin(), wordList.end(), w) != wordList.end() && w.length() > longestWord.length()) {
                longestWord = w;
            }
        }
        return longestWord;
    }
};

int main() {
    LongestWord longestWord;
    longestWord.addWord("A");
    longestWord.addWord("aM");
    std::cout << longestWord.findLongestWord("I am a student.") << std::endl;
    return 0;
}