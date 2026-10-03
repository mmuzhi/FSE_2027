#include <vector>
#include <string>
#include <unordered_set>

class NLPDataProcessor {
public:
    std::vector<std::string> constructStopWordList() {
        return {"a", "an", "the"};
    }

    std::vector<std::vector<std::string>> removeStopWords(const std::vector<std::string>& stringList, const std::vector<std::string>& stopWordList) {
        std::vector<std::vector<std::string>> result;
        std::unordered_set<std::string> stopSet(stopWordList.begin(), stopWordList.end());
        
        for (const std::string& str : stringList) {
            std::vector<std::string> words = splitSpace(str);
            std::vector<std::string> filteredWords;
            for (const std::string& word : words) {
                if (stopSet.find(word) == stopSet.end()) {
                    filteredWords.push_back(word);
                }
            }
            result.push_back(filteredWords);
        }
        return result;
    }

    std::vector<std::vector<std::string>> process(const std::vector<std::string>& stringList) {
        std::vector<std::string> stopWordList = constructStopWordList();
        return removeStopWords(stringList, stopWordList);
    }

private:
    std::vector<std::string> splitSpace(const std::string& str) {
        std::vector<std::string> tokens;
        std::string current;
        for (char c : str) {
            if (c == ' ') {
                tokens.push_back(current);
                current.clear();
            } else {
                current += c;
            }
        }
        tokens.push_back(current);
        while (!tokens.empty() && tokens.back().empty()) {
            tokens.pop_back();
        }
        return tokens;
    }
};