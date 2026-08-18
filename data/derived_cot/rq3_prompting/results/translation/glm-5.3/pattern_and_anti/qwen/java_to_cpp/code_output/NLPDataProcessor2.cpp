#include <algorithm>
#include <cctype>
#include <cstddef>
#include <functional>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace org {
namespace example {

class NLPDataProcessor2 {
public:
    class WordFrequency {
    public:
        const std::string word;
        const int frequency;

        WordFrequency(std::string word, int frequency)
            : word(std::move(word)), frequency(frequency) {}

        const std::string& getWord() const { return word; }
        int getFrequency() const { return frequency; }

        std::string toString() const {
            return "WordFrequency{word='" + word + "', frequency=" +
                   std::to_string(frequency) + "}";
        }

        bool operator==(const WordFrequency& other) const {
            return frequency == other.frequency && word == other.word;
        }

        bool operator!=(const WordFrequency& other) const {
            return !(*this == other);
        }

        std::size_t hashCode() const {
            std::size_t h = std::hash<std::string>{}(word);
            h = 31 * h + std::hash<int>{}(frequency);
            return h;
        }

        // Equivalent of byFrequencyThenWord(): frequency descending, then word ascending.
        static bool byFrequencyThenWord(const WordFrequency& a, const WordFrequency& b) {
            if (a.frequency != b.frequency) return a.frequency > b.frequency;
            return a.word < b.word;
        }
    };

    std::vector<std::vector<std::string>> processData(
            const std::vector<std::string>& stringList) const {
        std::vector<std::vector<std::string>> wordsList;
        wordsList.reserve(stringList.size());

        for (const std::string& str : stringList) {
            // toLowerCase(), then remove [^a-zA-Z\s] in a single pass.
            std::string processed;
            processed.reserve(str.size());
            for (char ch : str) {
                char lower = static_cast<char>(std::tolower(static_cast<unsigned char>(ch)));
                unsigned char u = static_cast<unsigned char>(lower);
                bool isLetter = (u >= 'a' && u <= 'z') || (u >= 'A' && u <= 'Z');
                if (isLetter || isJavaSpace(u)) {
                    processed.push_back(lower);
                }
            }
            wordsList.push_back(processed.empty()
                ? std::vector<std::string>{}
                : splitOnWhitespace(processed));
        }
        return wordsList;
    }

    std::vector<WordFrequency> calculateWordFrequency(
            const std::vector<std::vector<std::string>>& wordsList) const {
        // LinkedHashMap semantics: hash lookup + insertion-order iteration.
        std::unordered_map<std::string, int> frequencyMap;
        std::unordered_map<std::string, int> orderMap;   // word -> first-seen index
        std::vector<std::string> insertionOrder;         // mirrors frequencyMap key order
        int index = 0;

        for (const auto& words : wordsList) {
            for (const auto& word : words) {
                if (frequencyMap.find(word) == frequencyMap.end()) {
                    orderMap.emplace(word, index++);
                    insertionOrder.push_back(word);
                }
                ++frequencyMap[word];
            }
        }

        std::vector<WordFrequency> wordFrequencies;
        for (const auto& word : insertionOrder) {
            int frequency = frequencyMap[word];
            if (frequency > 1 || word == "%%%") {
                wordFrequencies.emplace_back(word, frequency);
            }
        }

        std::sort(wordFrequencies.begin(), wordFrequencies.end(),
                  [&orderMap](const WordFrequency& wf1, const WordFrequency& wf2) {
                      if (wf1.getFrequency() != wf2.getFrequency()) {
                          return wf2.getFrequency() < wf1.getFrequency();
                      }
                      return orderMap.at(wf1.getWord()) < orderMap.at(wf2.getWord());
                  });

        return wordFrequencies;
    }

    std::vector<WordFrequency> process(const std::vector<std::string>& stringList) const {
        std::vector<std::vector<std::string>> wordsList = processData(stringList);
        return calculateWordFrequency(wordsList);
    }

private:
    // Java regex \s: exactly ' ', '\t', '\n', '\x0B', '\f', '\r'.
    static bool isJavaSpace(unsigned char c) {
        return c == ' ' || c == '\t' || c == '\n' ||
               c == '\v' || c == '\f' || c == '\r';
    }

    // Equivalent of String.split("\\s+") with default limit:
    // maximal whitespace runs as delimiters; a leading empty token is kept when
    // the string starts with whitespace; trailing empty tokens are dropped.
    static std::vector<std::string> splitOnWhitespace(const std::string& s) {
        std::vector<std::string> parts;
        std::size_t start = 0;
        std::size_t i = 0;
        while (i < s.size()) {
            if (isJavaSpace(static_cast<unsigned char>(s[i]))) {
                parts.push_back(s.substr(start, i - start));
                while (i < s.size() && isJavaSpace(static_cast<unsigned char>(s[i]))) {
                    ++i;
                }
                start = i;
            } else {
                ++i;
            }
        }
        parts.push_back(s.substr(start));
        while (!parts.empty() && parts.back().empty()) {
            parts.pop_back();
        }
        return parts;
    }
};

} // namespace example
} // namespace org

// Mirror of Java's equals/hashCode contract for use in hashed containers.
namespace std {
template <>
struct hash<org::example::NLPDataProcessor2::WordFrequency> {
    std::size_t operator()(
            const org::example::NLPDataProcessor2::WordFrequency& wf) const noexcept {
        return wf.hashCode();
    }
};
} // namespace std