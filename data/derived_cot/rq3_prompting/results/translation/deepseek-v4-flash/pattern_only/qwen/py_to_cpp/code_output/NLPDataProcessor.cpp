#include <vector>
#include <string>
#include <sstream>
#include <algorithm>

class NLPDataProcessor {
public:
    std::vector<std::string> construct_stop_word_list() {
        return {"a", "an", "the"};
    }

    std::vector<std::vector<std::string>> remove_stop_words(
        const std::vector<std::string>& string_list,
        const std::vector<std::string>& stop_word_list
    ) {
        std::vector<std::vector<std::string>> answer;

        for (const std::string& str : string_list) {
            std::vector<std::string> words;
            std::istringstream iss(str);
            std::string word;

            while (iss >> word) {
                words.push_back(word);
            }

            for (std::size_t i = 0; i < words.size(); ++i) {
                const std::string& current = words[i];
                if (std::find(stop_word_list.begin(), stop_word_list.end(), current) != stop_word_list.end()) {
                    auto it = std::find(words.begin(), words.end(), current);
                    if (it != words.end()) {
                        words.erase(it);
                    }
                }
            }

            answer.push_back(words);
        }

        return answer;
    }

    std::vector<std::vector<std::string>> process(const std::vector<std::string>& string_list) {
        std::vector<std::string> stop_word_list = construct_stop_word_list();
        return remove_stop_words(string_list, stop_word_list);
    }
};