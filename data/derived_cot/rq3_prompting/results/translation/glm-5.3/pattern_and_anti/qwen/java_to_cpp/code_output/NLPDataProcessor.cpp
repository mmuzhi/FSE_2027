#include <string>
#include <vector>
#include <algorithm>

class NLPDataProcessor {
public:
    std::vector<std::string> constructStopWordList() {
        return {"a", "an", "the"};
    }

    // Equivalent to Java's String.split(" ") with limit 0:
    // splits on every ' ', then drops trailing empty strings.
    static std::vector<std::string> splitOnSpace(const std::string& s) {
        if (s.find(' ') == std::string::npos) {
            // No delimiter found: Java returns [this] (even if s is empty -> [""]).
            return {s};
        }
        std::vector<std::string> parts;
        std::size_t start = 0;
        while (true) {
            std::size_t end = s.find(' ', start);
            if (end == std::string::npos) break;
            parts.push_back(s.substr(start, end - start));
            start = end + 1;
        }
        parts.push_back(s.substr(start));
        // Remove trailing empty strings (Java split semantics).
        while (!parts.empty() && parts.back().empty()) {
            parts.pop_back();
        }
        return parts;
    }

    std::vector<std::vector<std::string>> removeStopWords(
            const std::vector<std::string>& stringList,
            const std::vector<std::string>& stopWordList) {
        std::vector<std::vector<std::string>> result;
        for (const std::string& str : stringList) {
            std::vector<std::string> words;
            for (const std::string& word : splitOnSpace(str)) {
                // removeAll(stopWordList): drop words equal to any stop word, keep order.
                if (std::find(stopWordList.begin(), stopWordList.end(), word) == stopWordList.end()) {
                    words.push_back(word);
                }
            }
            result.push_back(words);
        }
        return result;
    }

    std::vector<std::vector<std::string>> process(const std::vector<std::string>& stringList) {
        std::vector<std::string> stopWordList = constructStopWordList();
        return removeStopWords(stringList, stopWordList);
    }
};