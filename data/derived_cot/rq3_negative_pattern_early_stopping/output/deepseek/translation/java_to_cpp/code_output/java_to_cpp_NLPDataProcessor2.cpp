#include <vector>
#include <string>
#include <regex>
#include <sstream>
#include <algorithm>
#include <unordered_map>
#include <cctype>

class NLPDataProcessor2 {
public:
    struct WordFrequency {
        std::string word;
        int frequency;

        WordFrequency(const std::string& word, int frequency)
            : word(word), frequency(frequency) {}
    };

    // Process data: remove non-letter, non-space characters, lower-case, then split
    std::vector<std::vector<std::string>> processData(const std::vector<std::string>& stringList) {
        std::vector<std::vector<std::string>> wordsList;
        std::regex pattern("[^a-zA-Z\\s]");

        for (const std::string& s : stringList) {
            // Convert to lower case (std::tolower works on unsigned char)
            std::string lowerStr = s;
            for (char& ch : lowerStr) {
                ch = static_cast<char>(std::tolower(static_cast<unsigned char>(ch)));
            }
            // Remove characters not in [a-zA-Z\s]
            std::string processed = std::regex_replace(lowerStr, pattern, "");
            
            // Split on whitespace
            std::vector<std::string> words;
            if (!processed.empty()) {
                std::istringstream stream(processed);
                std::string word;
                while (stream >> word) {
                    words.push_back(word);
                }
            }
            wordsList.push_back(std::move(words));
        }
        return wordsList;
    }

    // Calculate word frequencies and return sorted list
    std::vector<WordFrequency> calculateWordFrequency(const std::vector<std::vector<std::string>>& wordsList) {
        // Frequency map
        std::unordered_map<std::string, int> freqMap;
        // Order map: first occurrence index
        std::unordered_map<std::string, int> orderMap;
        // Vector to preserve first insertion order (like Java LinkedHashMap)
        std::vector<std::string> insertionOrder;
        int index = 0;

        for (const auto& words : wordsList) {
            for (const std::string& word : words) {
                if (freqMap.find(word) == freqMap.end()) {
                    // First time seeing this word
                    orderMap[word] = index++;
                    insertionOrder.push_back(word);
                }
                ++freqMap[word];
            }
        }

        std::vector<WordFrequency> result;
        for (const std::string& word : insertionOrder) {
            int freq = freqMap[word];
            // Include if frequency > 1 or word is "%%%"
            if (freq > 1 || word == "%%%") {
                result.emplace_back(word, freq);
            }
        }

        // Sort by descending frequency, then by ascending first occurrence order
        std::sort(result.begin(), result.end(),
            [&orderMap](const WordFrequency& a, const WordFrequency& b) {
                if (a.frequency != b.frequency)
                    return a.frequency > b.frequency; // descending
                return orderMap[a.word] < orderMap[b.word]; // ascending order
            }
        );

        return result;
    }

    // Convenience method: process data and compute frequencies
    std::vector<WordFrequency> process(const std::vector<std::string>& stringList) {
        auto wordsList = processData(stringList);
        return calculateWordFrequency(wordsList);
    }
};