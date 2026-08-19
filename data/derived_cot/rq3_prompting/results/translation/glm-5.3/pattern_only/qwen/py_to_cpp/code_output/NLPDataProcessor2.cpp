#include <algorithm>
#include <cctype>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

class NLPDataProcessor2 {
public:
    // Equivalent of Python's ordered dict (3.7+): preserves insertion order.
    using Dict = std::vector<std::pair<std::string, int>>;

    // keep only English letters and spaces, lowercase, split into words
    std::vector<std::vector<std::string>>
    process_data(const std::vector<std::string>& string_list) const {
        std::vector<std::vector<std::string>> words_list;
        words_list.reserve(string_list.size());
        for (const std::string& str : string_list) {
            // re.sub(r'[^a-zA-Z\s]', '', string.lower())
            std::string processed;
            processed.reserve(str.size());
            for (unsigned char ch : str) {
                unsigned char low = static_cast<unsigned char>(std::tolower(ch));
                if ((low >= 'a' && low <= 'z') || std::isspace(low)) {
                    processed += static_cast<char>(low);
                }
            }
            // str.split(): split on whitespace runs, drop empty tokens
            std::vector<std::string> words;
            std::string word;
            for (char c : processed) {
                if (std::isspace(static_cast<unsigned char>(c))) {
                    if (!word.empty()) {
                        words.push_back(word);
                        word.clear();
                    }
                } else {
                    word += c;
                }
            }
            if (!word.empty()) words.push_back(std::move(word));
            words_list.push_back(std::move(words));
        }
        return words_list;
    }

    // count words, sort by frequency descending (stable, first-seen order on ties), take top 5
    Dict
    calculate_word_frequency(const std::vector<std::vector<std::string>>& words_list) const {
        std::unordered_map<std::string, int> counts;
        std::vector<std::string> order;  // Counter insertion (first-encounter) order
        for (const auto& words : words_list) {
            for (const auto& w : words) {
                auto it = counts.find(w);
                if (it == counts.end()) {
                    counts.emplace(w, 1);
                    order.push_back(w);
                } else {
                    ++it->second;
                }
            }
        }
        // Python's sorted(..., key=x[1], reverse=True) is stable: equal counts
        // keep original order -> std::stable_sort with '>' matches exactly.
        std::vector<std::pair<std::string, int>> items;
        items.reserve(order.size());
        for (const auto& w : order) items.emplace_back(w, counts[w]);
        std::stable_sort(items.begin(), items.end(),
                         [](const std::pair<std::string, int>& a,
                            const std::pair<std::string, int>& b) {
                             return a.second > b.second;
                         });
        if (items.size() > 5) items.resize(5);  // [:5]
        return items;
    }

    Dict process(const std::vector<std::string>& string_list) const {
        auto words_list = process_data(string_list);
        return calculate_word_frequency(words_list);
    }
};