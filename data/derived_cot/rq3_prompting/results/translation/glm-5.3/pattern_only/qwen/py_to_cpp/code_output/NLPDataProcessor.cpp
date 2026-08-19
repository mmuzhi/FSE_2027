#include <algorithm>
#include <sstream>
#include <string>
#include <vector>

class NLPDataProcessor {
public:
    std::vector<std::string> construct_stop_word_list() {
        std::vector<std::string> stop_word_list = {"a", "an", "the"};
        return stop_word_list;
    }

    std::vector<std::vector<std::string>> remove_stop_words(
            const std::vector<std::string>& string_list,
            const std::vector<std::string>& stop_word_list) {
        std::vector<std::vector<std::string>> answer;
        for (const std::string& str : string_list) {
            // Python str.split(): split on whitespace runs, no empty tokens
            std::vector<std::string> string_split;
            std::istringstream iss(str);
            std::string tok;
            while (iss >> tok) {
                string_split.push_back(tok);
            }
            // Replicate Python's iterate-while-removing semantics:
            // index advances each step; list.remove deletes the FIRST match,
            // shifting later elements left (so the next element can be skipped).
            for (std::size_t i = 0; i < string_split.size(); ++i) {
                std::string word = string_split[i];
                if (std::find(stop_word_list.begin(), stop_word_list.end(), word)
                        != stop_word_list.end()) {
                    auto it = std::find(string_split.begin(), string_split.end(), word);
                    string_split.erase(it);
                }
            }
            answer.push_back(std::move(string_split));
        }
        return answer;
    }

    std::vector<std::vector<std::string>> process(const std::vector<std::string>& string_list) {
        std::vector<std::string> stop_word_list = construct_stop_word_list();
        std::vector<std::vector<std::string>> words_list =
            remove_stop_words(string_list, stop_word_list);
        return words_list;
    }
};