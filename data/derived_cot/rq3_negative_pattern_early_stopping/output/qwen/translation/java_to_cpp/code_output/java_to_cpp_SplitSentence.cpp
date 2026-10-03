#include <vector>
#include <string>
#include <regex>
#include <cctype>
#include <sstream>
#include <iostream>

class SplitSentence {
public:
    std::vector<std::string> splitSentences(const std::string& sentencesString) {
        std::vector<std::string> sentences;
        std::regex pattern(R"((?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s)");
        std::sregex_iterator it(sentencesString.begin(), sentencesString.end(), pattern);
        std::sregex_iterator end;

        std::size_t lastEnd = 0;
        while (it != end) {
            sentences.push_back(sentencesString.substr(lastEnd, it->str().size()));
            lastEnd = it->position() + it->str().size();
            ++it;
        }

        if (lastEnd < sentencesString.length()) {
            sentences.push_back(sentencesString.substr(lastEnd));
        }

        return sentences;
    }

    int countWords(const std::string& sentence) {
        std::string cleaned;
        for (char c : sentence) {
            if (std::isalnum(c) || c == ' ') {
                cleaned += c;
            }
        }
        std::istringstream iss(cleaned);
        std::string word;
        int count = 0;
        while (iss >> word) {
            count++;
        }
        return count;
    }

    int processTextFile(const std::string& sentencesString) {
        std::vector<std::string> sentences = splitSentences(sentencesString);
        int maxCount = 0;
        for (const auto& sentence : sentences) {
            int count = countWords(sentence);
            if (count > maxCount) {
                maxCount = count;
            }
        }
        return maxCount;
    }
};