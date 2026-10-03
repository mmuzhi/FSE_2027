#include <vector>
#include <string>
#include <map>
#include <algorithm>
#include <cctype>
#include <regex>
#include <sstream>
#include <utility>

class NLPDataProcessor2 {
public:
    std::vector<std::vector<std::string>> process_data(const std::vector<std::string>& string_list) {
        std::vector<std::vector<std::string>> words_list;
        std::regex non_english("[^a-zA-Z\\s]");
        for (const auto& s : string_list) {
            std::string lower;
            lower.reserve(s.size());
            for (char c : s) {
                lower.push_back(std::tolower(static_cast<unsigned char>(c)));
            }
            std::string cleaned = std::regex_replace(lower, non_english, "");
            std::istringstream stream(cleaned);
            std::vector<std::string> words;
            std::string word;
            while (stream >> word) {
                words.push_back(word);
            }
            words_list.push_back(words);
        }
        return words_list;
    }

    std::map<std::string, int> calculate_word_frequency(const std::vector<std::vector<std::string>>& words_list) {
        std::map<std::string, int> freq;
        for (const auto& words : words_list) {
            for (const auto& w : words) {
                freq[w]++;
            }
        }
        // Copy to vector of pairs
        std::vector<std::pair<std::string, int>> sorted(freq.begin(), freq.end());
        std::sort(sorted.begin(), sorted.end(),
            [](const std::pair<std::string, int>& a, const std::pair<std::string, int>& b) {
                if (a.second != b.second) return a.second > b.second;
                // Preserve insertion order? The original uses Counter which keeps first occurrence order.
                // Since we are sorting, we can't perfectly preserve original order if frequencies equal.
                // We'll fall back to key alphabetical ordering for deterministic behavior.
                return a.first < b.first;
            });
        // Take top 5
        std::map<std::string, int> top5;
        int count = 0;
        for (const auto& p : sorted) {
            if (count >= 5) break;
            top5[p.first] = p.second;
            ++count;
        }
        return top5;
    }

    std::map<std::string, int> process(const std::vector<std::string>& string_list) {
        auto words_list = process_data(string_list);
        return calculate_word_frequency(words_list);
    }
};