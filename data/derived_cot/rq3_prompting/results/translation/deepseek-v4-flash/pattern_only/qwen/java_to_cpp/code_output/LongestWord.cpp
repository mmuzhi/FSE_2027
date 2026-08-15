#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <cctype>

class LongestWord {
    std::vector<std::string> wordList;

public:
    LongestWord() {}

    void addWord(const std::string& word) {
        wordList.push_back(word);
    }

    std::string findLongestWord(const std::string& sentence) {
        std::string s = sentence;

        for (char& c : s) {
            c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
        }

        const std::string punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";
        s.erase(std::remove_if(s.begin(), s.end(),
            [&](char c) { return punctuation.find(c) != std::string::npos; }),
            s.end());

        std::vector<std::string> words;
        bool foundSpace = false;
        size_t start = 0;

        while (true) {
            size_t pos = s.find(' ', start);
            if (pos == std::string::npos) {
                words.push_back(s.substr(start));
                break;
            }
            foundSpace = true;
            words.push_back(s.substr(start, pos - start));
            start = pos + 1;
        }

        if (foundSpace) {
            while (!words.empty() && words.back().empty()) {
                words.pop_back();
            }
        }

        std::string longestWord;
        for (const std::string& word : words) {
            if (std::find(wordList.begin(), wordList.end(), word) != wordList.end() &&
                word.length() > longestWord.length()) {
                longestWord = word;
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