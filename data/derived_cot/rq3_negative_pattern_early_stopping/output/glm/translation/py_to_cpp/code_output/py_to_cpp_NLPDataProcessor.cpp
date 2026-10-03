#include <vector>
#include <string>
#include <algorithm>
#include <cctype>

class NLPDataProcessor {
public:
    std::vector<std::string> construct_stop_word_list() {
        return {"a", "an", "the"};
    }

    std::vector<std::vector<std::string>> remove_stop_words(
        const std::vector<std::string>& string_list,
        const std::vector<std::string>& stop_word_list) {

        std::vector<std::vector<std::string>> answer;

        for (const auto& str : string_list) {
            std::vector<std::string> string_split = split(str);

            size_t i = 0;
            while (i < string_split.size()) {
                const std::string& word = string_split[i];
                if (std::find(stop_word_list.begin(), stop_word_list.end(), word) != stop_word_list.end()) {
                    string_split.erase(string_split.begin() + i);
                    i++;
                } else {
                    i++;
                }
            }

            answer.push_back(string_split);
        }

        return answer;
    }

    std::vector<std::vector<std::string>> process(const std::vector<std::string>& string_list) {
        auto stop_word_list = construct_stop_word_list();
        return remove_stop_words(string_list, stop_word_list);
    }

private:
    std::vector<std::string> split(const std::string& s) {
        std::vector<std::string> tokens;
        std::string token;
        for (char c : s) {
            if (std::isspace(static_cast<unsigned char>(c))) {
                if (!token.empty()) {
                    tokens.push_back(token);
                    token.clear();
                }
            } else {
                token += c;
            }
        }
        if (!token.empty()) {
            tokens.push_back(token);
        }
        return tokens;
    }
};