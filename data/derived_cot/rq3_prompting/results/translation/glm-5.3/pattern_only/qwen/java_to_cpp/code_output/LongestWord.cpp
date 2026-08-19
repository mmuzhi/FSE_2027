#include <algorithm>
#include <cctype>
#include <iostream>
#include <string>
#include <vector>

namespace {
// Mirrors Java String.split(" ") with limit 0:
// - split at every single space, keeping interior empty tokens
// - if a match was found, drop trailing empty strings
// - if no match was found, return the whole input as the sole element (even "")
std::vector<std::string> splitOnSingleSpace(const std::string& s) {
    std::vector<std::string> words;
    size_t start = 0;
    bool matched = false;
    while (true) {
        size_t pos = s.find(' ', start);
        if (pos == std::string::npos) {
            break;
        }
        matched = true;
        words.push_back(s.substr(start, pos - start));
        start = pos + 1;
    }
    if (!matched) {
        words.push_back(s);
    } else {
        words.push_back(s.substr(start));
        while (!words.empty() && words.back().empty()) {
            words.pop_back();
        }
    }
    return words;
}
}  // namespace

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
        // Java: sentence.toLowerCase()
        for (char& c : sentence) {
            c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
        }
        // Java: remove all chars in [!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~]
        const std::string punct = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";
        sentence.erase(std::remove_if(sentence.begin(), sentence.end(),
                                      [&punct](char c) {
                                          return punct.find(c) != std::string::npos;
                                      }),
                       sentence.end());
        std::vector<std::string> words = splitOnSingleSpace(sentence);
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