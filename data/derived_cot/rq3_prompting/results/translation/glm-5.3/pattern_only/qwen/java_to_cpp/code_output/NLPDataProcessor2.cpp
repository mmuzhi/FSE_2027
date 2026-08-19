#include <algorithm>
#include <cctype>
#include <functional>
#include <sstream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace org::example {

class WordFrequency {
public:
    WordFrequency(std::string word, int frequency)
        : word_(std::move(word)), frequency_(frequency) {}

    const std::string& getWord() const { return word_; }
    int getFrequency() const { return frequency_; }

    std::string toString() const {
        std::ostringstream oss;
        oss << "WordFrequency{word='" << word_ << "', frequency=" << frequency_ << '}';
        return oss.str();
    }

    bool operator==(const WordFrequency& o) const {
        return frequency_ == o.frequency_ && word_ == o.word_;
    }
    bool operator!=(const WordFrequency& o) const { return !(*this == o); }

    // Mirrors byFrequencyThenWord(): frequency descending, then word ascending.
    static bool byFrequencyThenWord(const WordFrequency& a, const WordFrequency& b) {
        if (a.frequency_ != b.frequency_) return a.frequency_ > b.frequency_;
        return a.word_ < b.word_;
    }

private:
    const std::string word_;
    const int frequency_;
};

}  // namespace org::example

// Parity with hashCode() (hash specialization).
template <>
struct std::hash<org::example::WordFrequency> {
    std::size_t operator()(const org::example::WordFrequency& wf) const {
        std::size_t h1 = std::hash<std::string>{}(wf.getWord());
        std::size_t h2 = std::hash<int>{}(wf.getFrequency());
        return h1 ^ (h2 + 0x9e3779b9 + (h1 << 6) + (h1 >> 2));
    }
};

namespace org::example {

class NLPDataProcessor2 {
public:
    std::vector<std::vector<std::string>> processData(const std::vector<std::string>& stringList) const {
        std::vector<std::vector<std::string>> wordsList;
        wordsList.reserve(stringList.size());

        for (const std::string& str : stringList) {
            // toLowerCase()
            std::string lower;
            lower.reserve(str.size());
            for (char c : str) {
                lower += static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
            }
            // Remove [^a-zA-Z\s]
            std::string processed;
            processed.reserve(lower.size());
            for (char c : lower) {
                if (std::isalpha(static_cast<unsigned char>(c)) != 0 || isWhitespace(c)) {
                    processed += c;
                }
            }
            wordsList.push_back(splitOnWhitespaceRuns(processed));
        }
        return wordsList;
    }

    std::vector<WordFrequency> calculateWordFrequency(const std::vector<std::vector<std::string>>& wordsList) const {
        std::unordered_map<std::string, int> frequencyMap;
        std::unordered_map<std::string, int> orderMap;
        std::vector<std::string> insertionOrder;  // LinkedHashMap iteration order
        int index = 0;

        for (const std::vector<std::string>& words : wordsList) {
            for (const std::string& word : words) {
                auto it = frequencyMap.find(word);
                if (it == frequencyMap.end()) {
                    orderMap.emplace(word, index++);
                    insertionOrder.push_back(word);
                    frequencyMap.emplace(word, 1);
                } else {
                    ++it->second;
                }
            }
        }

        std::vector<WordFrequency> wordFrequencies;
        for (const std::string& word : insertionOrder) {
            int frequency = frequencyMap.at(word);
            if (frequency > 1 || word == "%%%") {
                wordFrequencies.emplace_back(word, frequency);
            }
        }

        std::sort(wordFrequencies.begin(), wordFrequencies.end(),
                  [&orderMap](const WordFrequency& wf1, const WordFrequency& wf2) {
                      if (wf1.getFrequency() != wf2.getFrequency()) {
                          return wf1.getFrequency() > wf2.getFrequency();
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
    // Java's \s character class.
    static bool isWhitespace(char c) {
        return c == ' ' || c == '\t' || c == '\n' || c == '\v' || c == '\f' || c == '\r';
    }

    // Replicates Java's String.split("\\s+") with limit 0:
    // - a leading whitespace run produces a leading "" token;
    // - trailing empty tokens are dropped;
    // - an all-whitespace string yields an empty list.
    static std::vector<std::string> splitOnWhitespaceRuns(const std::string& s) {
        std::vector<std::string> tokens;
        if (s.empty()) return tokens;  // List.of() case
        if (isWhitespace(s[0])) tokens.emplace_back("");
        std::string current;
        bool inToken = false;
        for (char c : s) {
            if (isWhitespace(c)) {
                if (inToken) {
                    tokens.push_back(current);
                    current.clear();
                    inToken = false;
                }
            } else {
                current += c;
                inToken = true;
            }
        }
        if (inToken) tokens.push_back(current);
        while (!tokens.empty() && tokens.back().empty()) tokens.pop_back();
        return tokens;
    }
};

}  // namespace org::example