#include <vector>
#include <string>
#include <sstream>
#include <unordered_map>
#include <algorithm>
#include <cctype>
#include <utility>

class NLPDataProcessor2 {
public:
    std::vector<std::vector<std::string>> process_data(const std::vector<std::string>& string_list) {
        std::vector<std::vector<std::string>> words_list;
        for (const auto& str : string_list) {
            std::string processed_string;
            for (char c : str) {
                char lower_c = std::tolower(static_cast<unsigned char>(c));
                if ((lower_c >= 'a' && lower_c <= 'z') || std::isspace(static_cast<unsigned char>(c))) {
                    processed_string += lower_c;
                }
            }
            std::vector<std::string> words;
            std::istringstream iss(processed_string);
            std::string word;
            while (iss >> word) {
                words.push_back(word);
            }
            words_list.push_back(words);
        }
        return words_list;
    }

    std::vector<std::pair<std::string, int>> calculate_word_frequency(const std::vector<std::vector<std::string>>& words_list) {
        std::vector<std::string> order;
        std::unordered_map<std::string, int> counts;
        for (const auto& words : words_list) {
            for (const auto& word : words) {
                if (counts.find(word) == counts.end()) {
                    order.push_back(word);
                }
                counts[word]++;
            }
        }

        std::vector<std::pair<std::string, int>> word_frequency;
        for (const auto& word : order) {
            word_frequency.emplace_back(word, counts[word]);
        }

        std::stable_sort(word_frequency.begin(), word_frequency.end(), [](const auto& a, const auto& b) {
            return a.second > b.second;
        });

        if (word_frequency.size() > 5) {
            word_frequency.resize(5);
        }

        return word_frequency;
    }

    std::vector<std::pair<std::string, int>> process(const std::vector<std::string>& string_list) {
        auto words_list = process_data(string_list);
        return calculate_word_frequency(words_list);
    }
};