#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
#include <cctype> // For std::isspace

struct NLPDataProcessor {
    // Returns a vector of stop words
    std::vector<std::string> constructStopWordList() const {
        return {"a", "an", "the"};
    }

    // Removes stop words from each string in the list
    std::vector<std::vector<std::string>> removeStopWords(
        const std::vector<std::string>& stringList,
        const std::vector<std::string>& stopWordList
    ) const {
        std::vector<std::vector<std::string>> result;
        result.reserve(stringList.size()); // Reserve space for efficiency

        for (const auto& s : stringList) {
            std::vector<std::string> words;
            std::istringstream iss(s);
            std::string word;
            while (iss >> word) {
                words.push_back(word);
            }

            // Remove all occurrences of stop words
            words.erase(
                std::remove_if(words.begin(), words.end(),
                    [&stopWordList](const std::string& w) {
                        return std::find(stopWordList.begin(), stopWordList.end(), w) != stopWordList.end();
                    }),
                words.end()
            );
            result.push_back(words);
        }
        return result;
    }

    // Main processing function
    std::vector<std::vector<std::string>> process(
        const std::vector<std::string>& stringList
    ) const {
        auto stopWordList = constructStopWordList();
        return removeStopWords(stringList, stopWordList);
    }
};