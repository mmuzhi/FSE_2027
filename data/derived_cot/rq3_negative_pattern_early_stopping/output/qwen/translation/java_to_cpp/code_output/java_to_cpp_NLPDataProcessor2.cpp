#include <vector>
#include <string>
#include <regex>
#include <unordered_map>
#include <algorithm>
#include <sstream>
#include <cctype>
#include <locale>

struct WordFrequency {
    std::string word;
    int frequency;

    WordFrequency(const std::string& word, int frequency) : word(word), frequency(frequency) {}

    // We don't need getters because we can access directly, but if we want to mimic the Java code, we can add them.
    // However, the problem says to keep behavior identical, and the Java code has getters. But in C++, we can access directly.
    // But note: the comparator in Java uses getWord. We can either use direct access or add getters. Let's add getters for consistency.

    std::string getWord() const { return word; }
    int getFrequency() const { return frequency; }
};

// We'll define the NLPDataProcessor2 class
class NLPDataProcessor2 {
public:
    static std::vector<std::vector<std::string>> processData(const std::vector<std::string>& stringList) {
        std::regex pattern("[^a-zA-Z\\s]");
        std::vector<std::vector<std::string>> wordsList;

        for (const auto& s : stringList) {
            std::string processedString = std::regex_replace(s, pattern, "");
            std::istringstream iss(processedString);
            std::vector<std::string> words;
            std::string word;
            while (iss >> word) {
                words.push_back(word);
            }
            wordsList.push_back(words);
        }
        return wordsList;
    }

    static std::vector<WordFrequency> calculateWordFrequency(const std::vector<std::vector<std::string>>& wordsList) {
        std::unordered_map<std::string, int> frequencyMap;
        std::unordered_map<std::string, int> orderMap;
        int index = 0;

        for (const auto& words : wordsList) {
            for (const auto& word : words) {
                if (orderMap.find(word) == orderMap.end()) {
                    orderMap[word] = index++;
                }
                frequencyMap[word]++;
            }
        }

        std::vector<WordFrequency> wordFrequencies;
        for (const auto& entry : frequencyMap) {
            const std::string& word = entry.first;
            int frequency = entry.second;
            if (frequency > 1 || word == "%%%") {
                wordFrequencies.push_back(WordFrequency(word, frequency));
            }
        }

        // Sort by frequency descending, then by the order of first occurrence (index in orderMap)
        std::sort(wordFrequencies.begin(), wordFrequencies.end(), [&orderMap](const WordFrequency& wf1, const WordFrequency& wf2) {
            if (wf2.frequency != wf1.frequency) {
                return wf2.frequency > wf1.frequency;
            }
            // Compare by the index in orderMap
            int index1 = orderMap.at(wf1.word);
            int index2 = orderMap.at(wf2.word);
            return index1 < index2;
        });

        return wordFrequencies;
    }

    static std::vector<WordFrequency> process(const std::vector<std::string>& stringList) {
        std::vector<std::vector<std::string>> wordsList = processData(stringList);
        return calculateWordFrequency(wordsList);
    }
};