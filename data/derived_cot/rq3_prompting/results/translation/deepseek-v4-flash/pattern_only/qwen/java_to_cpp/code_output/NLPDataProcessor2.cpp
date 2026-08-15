#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <sstream>
#include <cstdint>
#include <utility>

class NLPDataProcessor2 {
public:
    class WordFrequency {
    private:
        std::string word;
        int frequency;

    public:
        WordFrequency(std::string word, int frequency)
            : word(std::move(word)), frequency(frequency) {}

        const std::string& getWord() const {
            return word;
        }

        int getFrequency() const {
            return frequency;
        }

        std::string toString() const {
            std::ostringstream oss;
            oss << "WordFrequency{word='" << word << "', frequency=" << frequency << '}';
            return oss.str();
        }

        bool equals(const WordFrequency& other) const {
            return frequency == other.frequency && word == other.word;
        }

        bool operator==(const WordFrequency& other) const {
            return equals(other);
        }

        bool operator!=(const WordFrequency& other) const {
            return !equals(other);
        }

        int hashCode() const {
            uint32_t h = 0;
            for (unsigned char c : word) {
                h = h * 31 + c;
            }
            uint32_t result = 31 * (31 + h) + static_cast<uint32_t>(frequency);
            return static_cast<int>(result);
        }

        struct FrequencyThenWordComparator {
            bool operator()(const WordFrequency& a, const WordFrequency& b) const {
                if (a.frequency != b.frequency) {
                    return a.frequency > b.frequency;
                }
                return a.word < b.word;
            }
        };

        static FrequencyThenWordComparator byFrequencyThenWord() {
            return FrequencyThenWordComparator();
        }
    };

    std::vector<std::vector<std::string>> processData(const std::vector<std::string>& stringList) const {
        std::vector<std::vector<std::string>> wordsList;
        for (const std::string& str : stringList) {
            std::string processed;
            for (unsigned char c : str) {
                char ch = static_cast<char>(c);
                if (ch >= 'A' && ch <= 'Z') {
                    ch += 'a' - 'A';
                }
                if (isAsciiLetter(ch) || isJavaWhitespace(ch)) {
                    processed += ch;
                }
            }

            std::vector<std::string> words;
            if (!processed.empty()) {
                words = splitJavaWhitespace(processed);
            }
            wordsList.push_back(std::move(words));
        }
        return wordsList;
    }

    std::vector<WordFrequency> calculateWordFrequency(
        const std::vector<std::vector<std::string>>& wordsList) const {
        std::vector<std::string> order;
        std::unordered_map<std::string, int> frequencyMap;
        std::unordered_map<std::string, int> orderMap;
        int index = 0;

        for (const auto& words : wordsList) {
            for (const std::string& word : words) {
                if (frequencyMap.find(word) == frequencyMap.end()) {
                    orderMap[word] = index++;
                    order.push_back(word);
                }
                frequencyMap[word] = frequencyMap[word] + 1;
            }
        }

        std::vector<WordFrequency> wordFrequencies;
        for (const std::string& word : order) {
            int frequency = frequencyMap[word];
            if (frequency > 1 || word == "%%%") {
                wordFrequencies.emplace_back(word, frequency);
            }
        }

        std::sort(wordFrequencies.begin(), wordFrequencies.end(),
            [&](const WordFrequency& a, const WordFrequency& b) {
                if (a.getFrequency() != b.getFrequency()) {
                    return a.getFrequency() > b.getFrequency();
                }
                return orderMap.at(a.getWord()) < orderMap.at(b.getWord());
            });

        return wordFrequencies;
    }

    std::vector<WordFrequency> process(const std::vector<std::string>& stringList) const {
        std::vector<std::vector<std::string>> wordsList = processData(stringList);
        return calculateWordFrequency(wordsList);
    }

private:
    static bool isAsciiLetter(char c) {
        return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z');
    }

    static bool isJavaWhitespace(char c) {
        return c == ' ' || c == '\t' || c == '\n' || c == '\v' || c == '\f' || c == '\r';
    }

    static std::vector<std::string> splitJavaWhitespace(const std::string& s) {
        if (s.empty()) {
            return {""};
        }

        std::vector<std::string> tokens;
        size_t i = 0;
        while (i < s.size()) {
            if (!isJavaWhitespace(s[i])) {
                size_t start = i;
                while (i < s.size() && !isJavaWhitespace(s[i])) {
                    ++i;
                }
                tokens.emplace_back(s.substr(start, i - start));
            } else {
                ++i;
            }
        }

        if (tokens.empty()) {
            return {};
        }

        std::vector<std::string> result;
        if (isJavaWhitespace(s[0])) {
            result.emplace_back("");
        }
        result.insert(result.end(), tokens.begin(), tokens.end());
        return result;
    }
};