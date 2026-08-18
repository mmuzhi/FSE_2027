#include <algorithm>
#include <cctype>
#include <sstream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

class NLPDataProcessor2 {
public:
    // Ordered dictionary equivalent: vector of (word, frequency) pairs,
    // sorted by frequency descending (stable, ties keep first-seen order).
    using WordFrequency = std::vector<std::pair<std::string, int>>;

    std::vector<std::vector<std::string>> process_data(const std::vector<std::string>& string_list) const {
        std::vector<std::vector<std::string>> words_list;
        words_list.reserve(string_list.size());
        for (const std::string& str : string_list) {
            // Lowercase, then keep only English letters and whitespace
            // (equivalent to re.sub(r'[^a-zA-Z\s]', '', string.lower()) for ASCII input).
            std::string processed;
            processed.reserve(str.size());
            for (char ch : str) {
                unsigned char c = static_cast<unsigned char>(ch);
                c = static_cast<unsigned char>(std::tolower(c));
                if (std::isalpha(c) != 0 || std::isspace(c) != 0) {
                    processed += static_cast<char>(c);
                }
            }
            // Split on whitespace.
            std::vector<std::string> words;
            std::istringstream iss(processed);
            std::string token;
            while (iss >> token) {
                words.push_back(token);
            }
            words_list.push_back(std::move(words));
        }
        return words_list;
    }

    WordFrequency calculate_word_frequency(const std::vector<std::vector<std::string>>& words_list) const {
        // Counter equivalent: counts plus first-insertion order.
        std::unordered_map<std::string, int> word_frequency;
        std::vector<std::string> order;
        for (const std::vector<std::string>& words : words_list) {
            for (const std::string& w : words) {
                auto it = word_frequency.find(w);
                if (it == word_frequency.end()) {
                    word_frequency.emplace(w, 1);
                    order.push_back(w);
                } else {
                    ++it->second;
                }
            }
        }
        // Build items in insertion order, then stable sort by value descending
        // (matches Python's stable sorted(..., reverse=True)).
        WordFrequency sorted_word_frequency;
        sorted_word_frequency.reserve(order.size());
        for (const std::string& w : order) {
            sorted_word_frequency.emplace_back(w, word_frequency[w]);
        }
        std::stable_sort(sorted_word_frequency.begin(), sorted_word_frequency.end(),
                         [](const std::pair<std::string, int>& a, const std::pair<std::string, int>& b) {
                             return a.second > b.second;
                         });
        // Take top 5 entries.
        if (sorted_word_frequency.size() > 5) {
            sorted_word_frequency.resize(5);
        }
        return sorted_word_frequency;
    }

    WordFrequency process(const std::vector<std::string>& string_list) const {
        std::vector<std::vector<std::string>> words_list = process_data(string_list);
        return calculate_word_frequency(words_list);
    }
};