#include <vector>
#include <string>
#include <sstream>
#include <algorithm>

class NLPDataProcessor {
public:
    std::vector<std::string> constructStopWordList() {
        return {"a", "an", "the"};
    }

    std::vector<std::vector<std::string>> removeStopWords(
        const std::vector<std::string>& stringList,
        const std::vector<std::string>& stopWordList) 
    {
        std::vector<std::vector<std::string>> result;
        for (const auto& s : stringList) {
            std::vector<std::string> words;
            std::istringstream iss(s);
            std::string token;
            while (std::getline(iss, token, ' ')) {
                words.push_back(token);
            }
            // Remove all occurrences of any stop word
            for (const auto& stop : stopWordList) {
                words.erase(std::remove(words.begin(), words.end(), stop), words.end());
            }
            result.push_back(words);
        }
        return result;
    }

    std::vector<std::vector<std::string>> process(
        const std::vector<std::string>& stringList) 
    {
        std::vector<std::string> stopWordList = constructStopWordList();
        return removeStopWords(stringList, stopWordList);
    }
};