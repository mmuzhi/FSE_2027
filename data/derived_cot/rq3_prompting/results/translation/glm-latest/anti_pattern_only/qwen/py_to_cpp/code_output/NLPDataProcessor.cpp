#include <algorithm>
#include <cstddef>
#include <sstream>
#include <string>
#include <vector>

class NLPDataProcessor {
public:
    /**
     * Construct a stop word list including 'a', 'an', 'the'.
     * @return a list of stop words
     */
    std::vector<std::string> constructStopWordList() const {
        std::vector<std::string> stopWordList = {"a", "an", "the"};
        return stopWordList;
    }

    /**
     * Remove all the stop words from the list of strings.
     * @param stringList a list of strings
     * @param stopWordList a list of stop words
     * @return a list of words without stop words
     */
    std::vector<std::vector<std::string>> removeStopWords(
        const std::vector<std::string>& stringList,
        const std::vector<std::string>& stopWordList) const {

        std::vector<std::vector<std::string>> answer;
        answer.reserve(stringList.size());

        for (const std::string& str : stringList) {
            // Equivalent of Python's str.split(): split on runs of
            // whitespace, ignoring leading/trailing whitespace.
            std::vector<std::string> stringSplit;
            std::istringstream iss(str);
            std::string word;
            while (iss >> word) {
                stringSplit.push_back(word);
            }

            // Mirrors Python's remove-while-iterating semantics: when an
            // element is erased, the element that shifts into its place
            // is skipped (the loop index always advances), so consecutive
            // stop words may not all be removed — exactly like the original.
            for (std::size_t i = 0; i < stringSplit.size(); ++i) {
                if (std::find(stopWordList.begin(), stopWordList.end(),
                              stringSplit[i]) != stopWordList.end()) {
                    stringSplit.erase(stringSplit.begin() +
                                      static_cast<std::ptrdiff_t>(i));
                }
            }

            answer.push_back(std::move(stringSplit));
        }
        return answer;
    }

    /**
     * Construct a stop word list including 'a', 'an', 'the', and remove all
     * the stop words from the list of strings.
     * @param stringList a list of strings
     * @return a list of words without stop words
     */
    std::vector<std::vector<std::string>> process(
        const std::vector<std::string>& stringList) const {
        std::vector<std::string> stopWordList = constructStopWordList();
        std::vector<std::vector<std::string>> wordsList =
            removeStopWords(stringList, stopWordList);
        return wordsList;
    }
};