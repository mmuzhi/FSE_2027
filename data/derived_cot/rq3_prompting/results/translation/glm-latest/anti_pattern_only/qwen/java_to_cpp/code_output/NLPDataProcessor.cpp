#include <algorithm>
#include <string>
#include <vector>

namespace org::example {

class NLPDataProcessor {
public:
    std::vector<std::string> constructStopWordList() const {
        return {"a", "an", "the"};
    }

    std::vector<std::vector<std::string>> removeStopWords(
            const std::vector<std::string>& stringList,
            const std::vector<std::string>& stopWordList) const {
        std::vector<std::vector<std::string>> result;
        result.reserve(stringList.size());
        for (const std::string& str : stringList) {
            std::vector<std::string> words = javaSplit(str, ' ');
            // Equivalent of List.removeAll(stopWordList)
            words.erase(std::remove_if(words.begin(), words.end(),
                                       [&stopWordList](const std::string& w) {
                                           return std::find(stopWordList.begin(),
                                                            stopWordList.end(),
                                                            w) != stopWordList.end();
                                       }),
                        words.end());
            result.push_back(std::move(words));
        }
        return result;
    }

    std::vector<std::vector<std::string>> process(const std::vector<std::string>& stringList) const {
        std::vector<std::string> stopWordList = constructStopWordList();
        return removeStopWords(stringList, stopWordList);
    }

private:
    // Mimics Java's String.split(" "): split on every single occurrence of the
    // delimiter, then discard trailing empty strings (only when at least one
    // split occurred; an input with no delimiter yields the whole string back).
    static std::vector<std::string> javaSplit(const std::string& s, char delimiter) {
        std::vector<std::string> parts;
        std::string current;
        for (char c : s) {
            if (c == delimiter) {
                parts.push_back(current);
                current.clear();
            } else {
                current.push_back(c);
            }
        }
        parts.push_back(current);

        if (s.find(delimiter) != std::string::npos) {
            while (!parts.empty() && parts.back().empty()) {
                parts.pop_back();
            }
        }
        return parts;
    }
};

} // namespace org::example