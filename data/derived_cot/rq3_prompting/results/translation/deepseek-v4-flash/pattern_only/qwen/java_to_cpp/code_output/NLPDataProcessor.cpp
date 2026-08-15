#include <vector>
#include <string>
#include <algorithm>

class NLPDataProcessor {
public:
    std::vector<std::string> constructStopWordList() {
        return {"a", "an", "the"};
    }

    std::vector<std::vector<std::string>> removeStopWords(
            const std::vector<std::string>& stringList,
            const std::vector<std::string>& stopWordList) {
        std::vector<std::vector<std::string>> result;
        for (const std::string& str : stringList) {
            std::vector<std::string> words = splitBySpace(str);
            std::vector<std::string> filtered;
            for (const std::string& word : words) {
                if (std::find(stopWordList.begin(), stopWordList.end(), word) == stopWordList.end()) {
                    filtered.push_back(word);
                }
            }
            result.push_back(filtered);
        }
        return result;
    }

    std::vector<std::vector<std::string>> process(const std::vector<std::string>& stringList) {
        std::vector<std::string> stopWordList = constructStopWordList();
        return removeStopWords(stringList, stopWordList);
    }

private:
    static std::vector<std::string> splitBySpace(const std::string& s) {
        if (s.empty()) {
            return {""};
        }
        std::vector<std::string> tokens;
        std::string::size_type start = 0;
        for (std::string::size_type i = 0; i <= s.size(); ++i) {
            if (i == s.size() || s[i] == ' ') {
                tokens.push_back(s.substr(start, i - start));
                start = i + 1;
            }
        }
        while (!tokens.empty() && tokens.back().empty()) {
            tokens.pop_back();
        }
        return tokens;
    }
};