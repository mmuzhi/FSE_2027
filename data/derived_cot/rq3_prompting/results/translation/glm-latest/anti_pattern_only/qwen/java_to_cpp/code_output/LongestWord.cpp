#include <algorithm>
#include <cctype>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

class LongestWord {
public:
    LongestWord() = default;

    void addWord(const std::string& word) {
        wordList.push_back(word);
    }

    std::string findLongestWord(std::string sentence) const {
        std::string longestWord;

        // sentence.toLowerCase()
        std::transform(sentence.begin(), sentence.end(), sentence.begin(),
                       [](unsigned char c) { return static_cast<char>(std::tolower(c)); });

        // remove all punctuation: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        static const std::string punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";
        sentence.erase(std::remove_if(sentence.begin(), sentence.end(),
                                      [](unsigned char c) {
                                          return punctuation.find(static_cast<char>(c)) != std::string::npos;
                                      }),
                       sentence.end());

        // split on single spaces, dropping trailing empty tokens (Java's split(" "))
        std::vector<std::string> words;
        std::string token;
        std::istringstream iss(sentence);
        while (std::getline(iss, token, ' ')) {
            words.push_back(token);
        }
        while (!words.empty() && words.back().empty()) {
            words.pop_back();
        }

        for (const std::string& word : words) {
            if (std::find(wordList.begin(), wordList.end(), word) != wordList.end() &&
                word.length() > longestWord.length()) {
                longestWord = word;
            }
        }
        return longestWord;
    }

private:
    std::vector<std::string> wordList;
};

int main() {
    LongestWord longestWord;
    longestWord.addWord("A");
    longestWord.addWord("aM");
    std::cout << longestWord.findLongestWord("I am a student.") << std::endl;
    return 0;
}