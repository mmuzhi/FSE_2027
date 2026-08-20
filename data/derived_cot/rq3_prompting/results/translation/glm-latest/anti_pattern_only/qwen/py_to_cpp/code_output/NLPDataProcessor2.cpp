#include <algorithm>
#include <sstream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

class NLPDataProcessor2 {
public:
    // Keep only English letters and spaces in the string, then convert the
    // string to lower case, and then split the string into a list of words.
    // Returns a list of words lists.
    std::vector<std::vector<std::string>>
    process_data(const std::vector<std::string>& string_list) const {
        std::vector<std::vector<std::string>> words_list;
        words_list.reserve(string_list.size());
        for (const std::string& str : string_list) {
            // Remove non-English letters and convert to lowercase
            // (equivalent to re.sub(r'[^a-zA-Z\s]', '', string.lower()))
            std::string processed_string;
            processed_string.reserve(str.size());
            for (char c : str) {
                unsigned char uc = static_cast<unsigned char>(c);
                // ASCII-only tolower (locale independent)
                if (uc >= 'A' && uc <= 'Z') {
                    uc = static_cast<unsigned char>(uc - 'A' + 'a');
                }
                // keep only [a-z] or whitespace (\s = space \t \n \v \f \r)
                if ((uc >= 'a' && uc <= 'z') || is_ascii_space(uc)) {
                    processed_string.push_back(static_cast<char>(uc));
                }
            }

            // Split the string into words (like Python's str.split():
            // any run of whitespace separates words, empties discarded)
            std::vector<std::string> words;
            std::istringstream iss(processed_string);
            std::string word;
            while (iss >> word) {
                words.push_back(word);
            }
            words_list.push_back(std::move(words));
        }
        return words_list;
    }

    // Calculate the word frequency of each word in the list of words list,
    // sort by frequency in descending order, and return the top 5 entries.
    // The result is an ordered mapping (word -> frequency); ties keep the
    // order of first encounter, matching Python's Counter (insertion order)
    // combined with sorted()'s stable sort.
    std::vector<std::pair<std::string, int>>
    calculate_word_frequency(const std::vector<std::vector<std::string>>& words_list) const {
        std::unordered_map<std::string, int> word_frequency;
        std::vector<std::string> insertion_order; // Counter preserves insertion order

        for (const std::vector<std::string>& words : words_list) {
            for (const std::string& word : words) {
                auto it = word_frequency.find(word);
                if (it == word_frequency.end()) {
                    word_frequency.emplace(word, 1);
                    insertion_order.push_back(word);
                } else {
                    ++it->second;
                }
            }
        }

        // Build items in insertion order, then stable-sort by value descending.
        std::vector<std::pair<std::string, int>> items;
        items.reserve(insertion_order.size());
        for (const std::string& word : insertion_order) {
            items.emplace_back(word, word_frequency.at(word));
        }
        std::stable_sort(items.begin(), items.end(),
                         [](const std::pair<std::string, int>& a,
                            const std::pair<std::string, int>& b) {
                             return a.second > b.second;
                         });

        // Keep only the top 5 entries.
        if (items.size() > 5) {
            items.resize(5);
        }
        return items;
    }

    // process_data followed by calculate_word_frequency.
    // Returns the top 5 word frequency mapping (word -> frequency).
    std::vector<std::pair<std::string, int>>
    process(const std::vector<std::string>& string_list) const {
        std::vector<std::vector<std::string>> words_list = process_data(string_list);
        return calculate_word_frequency(words_list);
    }

private:
    // Matches Python's ASCII \s class: [ \t\n\r\f\v]
    static bool is_ascii_space(unsigned char c) {
        return c == ' ' || c == '\t' || c == '\n' ||
               c == '\v' || c == '\f' || c == '\r';
    }
};