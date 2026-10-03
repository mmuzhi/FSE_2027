#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <cctype>
#include <regex>

class LongestWord {
private:
    std::vector<std::string> wordList;

public:
    LongestWord() = default;

    void addWord(const std::string& word) {
        wordList.push_back(word);
    }

    std::string findLongestWord(std::string sentence) {
        std::string longestWord;
        // Convert to lowercase
        std::transform(sentence.begin(), sentence.end(), sentence.begin(), ::tolower);
        // Remove punctuation: characters in !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        // Escape special regex characters: quote them
        std::string punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";
        std::string escapedPunctuation;
        for (char c : punctuation) {
            escapedPunctuation += '\\';
            escapedPunctuation += c;
        }
        std::regex re("[" + escapedPunctuation + "]");
        sentence = std::regex_replace(sentence, re, "");
        // Split by spaces
        std::istringstream stream(sentence);
        std::string word;
        while (stream >> word) {
            // Check if word is in wordList and longer than current longest
            if (std::find(wordList.begin(), wordList.end(), word) != wordList.end()) {
                if (word.length() > longestWord.length()) {
                    longestWord = word;
                }
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