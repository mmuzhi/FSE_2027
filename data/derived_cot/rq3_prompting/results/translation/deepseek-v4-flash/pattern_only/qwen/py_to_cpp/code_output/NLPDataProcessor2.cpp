#include <vector>
#include <string>
#include <sstream>
#include <unordered_map>
#include <algorithm>
#include <utility>

class NLPDataProcessor2 {
public:
    using WordsList = std::vector<std::vector<std::string>>;
    using WordFrequencyDict = std::vector<std::pair<std::string, int>>;

    WordsList process_data(const std::vector<std::string>& string_list) const {
        WordsList words_list;
        words_list.reserve(string_list.size());

        for (const std::string& str : string_list) {
            std::string processed;
            processed.reserve(str.size());

            for (char c : str) {
                if (is_alpha(c) || is_space(c)) {
                    processed.push_back(to_lower(c));
                }
            }

            std::istringstream iss(processed);
            std::vector<std::string> words;
            std::string word;
            while (iss >> word) {
                words.push_back(word);
            }

            words_list.push_back(std::move(words));
        }

        return words_list;
    }

    WordFrequencyDict calculate_word_frequency(const WordsList& words_list) const {
        std::unordered_map<std::string, int> freq;
        std::unordered_map<std::string, int> order;
        int next_order = 0;

        for (const auto& words : words_list) {
            for (const std::string& word : words) {
                if (freq.find(word) == freq.end()) {
                    order[word] = next_order++;
                }
                ++freq[word];
            }
        }

        WordFrequencyDict result;
        result.reserve(freq.size());

        for (const auto& kv : freq) {
            result.emplace_back(kv.first, kv.second);
        }

        std::sort(result.begin(), result.end(),
            [&order](const std::pair<std::string, int>& a,
                     const std::pair<std::string, int>& b) {
                if (a.second != b.second) {
                    return a.second > b.second;
                }
                return order.at(a.first) < order.at(b.first);
            });

        if (result.size() > 5) {
            result.resize(5);
        }

        return result;
    }

    WordFrequencyDict process(const std::vector<std::string>& string_list) const {
        WordsList words_list = process_data(string_list);
        return calculate_word_frequency(words_list);
    }

private:
    static bool is_alpha(char c) {
        return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z');
    }

    static bool is_space(char c) {
        return c == ' ' || c == '\t' || c == '\n' || c == '\v' || c == '\f' || c == '\r';
    }

    static char to_lower(char c) {
        if (c >= 'A' && c <= 'Z') {
            return c - 'A' + 'a';
        }
        return c;
    }
};