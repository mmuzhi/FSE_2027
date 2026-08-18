#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <cctype>

class LongestWord {
private:
    std::vector<std::string> wordList;

public:
    LongestWord() = default;

    void addWord(const std::string& word) {
        wordList.push_back(word);
    }

    std::string findLongestWord(std::string sentence) {
        std::string longestWord = "";

        // sentence.toLowerCase()
        for (char& c : sentence) {
            c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
        }

        // remove all punctuation: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        static const std::string punct = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";
        std::string cleaned;
        for (char c : sentence) {
            if (punct.find(c) == std::string::npos) {
                cleaned += c;
            }
        }

        // Java split(" "): split on single spaces; trailing empty tokens removed
        std::vector<std::string> words;
        std::string token;
        for (char c : cleaned) {
            if (c == ' ') {
                words.push_back(token);
                token.clear();
            } else {
                token += c;
            }
        }
        words.push_back(token);
        while (!words.empty() && words.back().empty()) {
            words.pop_back();
        }

        for (const std::string& word : words) {
            bool contains = std::find(wordList.begin(), wordList.end(), word) != wordList.end();
            if (contains && word.length() > longestWord.length()) {
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