#include <string>
#include <vector>
#include <regex>
#include <unordered_map>
#include <algorithm>
#include <cctype>
#include <functional>

class NLPDataProcessor2 {
public:
    class WordFrequency {
    public:
        std::string word;
        int frequency;

        WordFrequency(std::string word, int frequency)
            : word(std::move(word)), frequency(frequency) {}

        const std::string& getWord() const { return word; }
        int getFrequency() const { return frequency; }

        std::string toString() const {
            return "WordFrequency{word='" + word + "', frequency=" + std::to_string(frequency) + '}';
        }

        bool equals(const WordFrequency& that) const {
            return frequency == that.frequency && word == that.word;
        }

        bool operator==(const WordFrequency& that) const {
            return equals(that);
        }

        size_t hashCode() const {
            size_t result = 1;
            result = 31 * result + std::hash<std::string>{}(word);
            result = 31 * result + std::hash<int>{}(frequency);
            return result;
        }

        static std::function<bool(const WordFrequency&, const WordFrequency&)> byFrequencyThenWord() {
            return [](const WordFrequency& wf1, const WordFrequency& wf2) {
                if (wf1.frequency != wf2.frequency) {
                    return wf2.frequency < wf1.frequency;
                }
                return wf1.word < wf2.word;
            };
        }
    };

    std::vector<std::vector<std::string>> processData(const std::vector<std::string>& stringList) {
        std::vector<std::vector<std::string>> wordsList;
        std::regex pattern("[^a-zA-Z\\s]");

        for (const std::string& str : stringList) {
            std::string lowerStr = str;
            std::transform(lowerStr.begin(), lowerStr.end(), lowerStr.begin(),
                           [](unsigned char c) { return std::tolower(c); });

            std::string processedString = std::regex_replace(lowerStr, pattern, "");

            std::vector<std::string> words;
            if (!processedString.empty()) {
                std::regex spaceRegex("\\s+");
                std::sregex_token_iterator it(processedString.begin(), processedString.end(), spaceRegex, -1);
                std::sregex_token_iterator end;

                for (; it != end; ++it) {
                    words.push_back(it->str());
                }

                // Remove trailing empty strings to match Java's split("\\s+") behavior
                while (!words.empty() && words.back().empty()) {
                    words.pop_back();
                }
            }
            wordsList.push_back(words);
        }
        return wordsList;
    }

    std::vector<WordFrequency> calculateWordFrequency(const std::vector<std::vector<std::string>>& wordsList) {
        // LinkedHashMap equivalent: track insertion order separately
        std::vector<std::string> insertionOrder;
        std::unordered_map<std::string, int> frequencyMap;
        std::unordered_map<std::string, int> orderMap;
        int index = 0;

        for (const auto& words : wordsList) {
            for (const std::string& word : words) {
                if (frequencyMap.find(word) == frequencyMap.end()) {
                    orderMap[word] = index++;
                    insertionOrder.push_back(word);
                }
                frequencyMap[word]++;
            }
        }

        std::vector<WordFrequency> wordFrequencies;
        for (const auto& word : insertionOrder) {
            int freq = frequencyMap[word];
            if (freq > 1 || word == "%%%") {
                wordFrequencies.emplace_back(word, freq);
            }
        }

        std::sort(wordFrequencies.begin(), wordFrequencies.end(),
            [&orderMap](const WordFrequency& wf1, const WordFrequency& wf2) {
                if (wf1.getFrequency() != wf2.getFrequency()) {
                    return wf1.getFrequency() > wf2.getFrequency();
                }
                return orderMap[wf1.getWord()] < orderMap[wf2.getWord()];
            });

        return wordFrequencies;
    }

    std::vector<WordFrequency> process(const std::vector<std::string>& stringList) {
        std::vector<std::vector<std::string>> wordsList = processData(stringList);
        return calculateWordFrequency(wordsList);
    }
};