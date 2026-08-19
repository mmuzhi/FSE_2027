#include <algorithm>
#include <string>
#include <vector>

class NLPDataProcessor {
public:
    std::vector<std::string> constructStopWordList() {
        return {"a", "an", "the"};
    }

    std::vector<std::vector<std::string>> removeStopWords(const std::vector<std::string>& stringList,
                                                          const std::vector<std::string>& stopWordList) {
        std::vector<std::vector<std::string>> result;
        for (const std::string& str : stringList) {
            std::vector<std::string> words = splitOnSpace(str);
            words.erase(std::remove_if(words.begin(), words.end(),
                                       [&stopWordList](const std::string& w) {
                                           return std::find(stopWordList.begin(), stopWordList.end(), w) != stopWordList.end();
                                       }),
                        words.end());
            result.push_back(std::move(words));
        }
        return result;
    }

    std::vector<std::vector<std::string>> process(const std::vector<std::string>& stringList) {
        std::vector<std::string> stopWordList = constructStopWordList();
        return removeStopWords(stringList, stopWordList);
    }

private:
    // Replicates Java's String.split(" "): keeps interior/leading empty tokens,
    // strips trailing empty tokens, and returns {s} when no delimiter is present
    // (including the empty string, which yields {""}).
    static std::vector<std::string> splitOnSpace(const std::string& s) {
        std::vector<std::string> tokens;
        size_t start = 0;
        bool matched = false;
        for (size_t i = 0; i < s.size(); ++i) {
            if (s[i] == ' ') {
                matched = true;
                tokens.push_back(s.substr(start, i - start));
                start = i + 1;
            }
        }
        if (!matched) {
            tokens.push_back(s);
            return tokens;
        }
        tokens.push_back(s.substr(start));
        while (!tokens.empty() && tokens.back().empty()) {
            tokens.pop_back();
        }
        return tokens;
    }
};