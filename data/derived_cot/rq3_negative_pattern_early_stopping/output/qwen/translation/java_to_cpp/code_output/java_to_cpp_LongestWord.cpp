#include <vector>
#include <string>
#include <cctype>
#include <algorithm>
#include <sstream>
#include <unordered_set>
#include <locale>
#include <cctype>
#include <regex>

class LongestWord {
private:
    std::vector<std::string> wordList;
    std::unordered_set<std::string> wordSet;

public:
    void addWord(const std::string& word) {
        wordList.push_back(word);
        wordSet.insert(word);
    }

    std::string findLongestWord(const std::string& sentence) {
        std::string cleaned;
        for (char c : sentence) {
            if (std::isalnum(c) || c == ' ') {
                cleaned += std::tolower(c, std::locale());
            }
        }
        std::istringstream iss(cleaned);
        std::string word;
        std::string longestWord = "";
        while (iss >> word) {
            if (wordSet.find(word) != wordSet.end() && word.length() > longestWord.length()) {
                longestWord = word;
            }
        }
        return longestWord;
    }
};

int main() {
    LongestWord lw;
    lw.addWord("A");
    lw.addWord("aM");
    std::cout << lw.findLongestWord("I am a student.") << std::endl;
    return 0;
}