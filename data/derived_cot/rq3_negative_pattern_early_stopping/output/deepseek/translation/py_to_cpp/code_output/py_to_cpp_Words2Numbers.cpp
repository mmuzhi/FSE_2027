#include <string>
#include <map>
#include <vector>
#include <sstream>
#include <algorithm>
#include <cctype>

class Words2Numbers {
private:
    std::map<std::string, std::pair<long long, long long>> numwords;
    std::vector<std::string> units = {
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen"
    };
    std::vector<std::string> tens = {"", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"};
    std::vector<std::string> scales = {"hundred", "thousand", "million", "billion", "trillion"};
    std::map<std::string, int> ordinal_words = {
        {"first", 1}, {"second", 2}, {"third", 3}, {"fifth", 5},
        {"eighth", 8}, {"ninth", 9}, {"twelfth", 12}
    };
    std::vector<std::pair<std::string, std::string>> ordinal_endings = {
        {"ieth", "y"}, {"th", ""}
    };

public:
    Words2Numbers() {
        numwords["and"] = {1, 0};
        for (size_t idx = 0; idx < units.size(); ++idx) {
            numwords[units[idx]] = {1, static_cast<long long>(idx)};
        }
        for (size_t idx = 0; idx < tens.size(); ++idx) {
            numwords[tens[idx]] = {1, static_cast<long long>(idx * 10)};
        }
        for (size_t idx = 0; idx < scales.size(); ++idx) {
            long long scale = 1;
            if (idx == 0) {
                scale = 100;
            } else {
                scale = 1;
                for (int i = 0; i < static_cast<int>(idx * 3); ++i) {
                    scale *= 10;
                }
            }
            numwords[scales[idx]] = {scale, 0};
        }
    }

    std::string text2int(const std::string& textnum) {
        std::string processed = textnum;
        std::replace(processed.begin(), processed.end(), '-', ' ');

        std::istringstream iss(processed);
        std::string word;
        long long current = 0, result = 0;
        std::string curstring;
        bool onnumber = false;

        while (iss >> word) {
            auto it = ordinal_words.find(word);
            if (it != ordinal_words.end()) {
                long long increment = it->second;
                current = current * 1 + increment;
                onnumber = true;
            } else {
                std::string modified = word;
                for (const auto& ending : ordinal_endings) {
                    if (modified.size() >= ending.first.size() &&
                        modified.substr(modified.size() - ending.first.size()) == ending.first) {
                        modified = modified.substr(0, modified.size() - ending.first.size()) + ending.second;
                        break;
                    }
                }

                auto num_it = numwords.find(modified);
                if (num_it == numwords.end()) {
                    if (onnumber) {
                        curstring += std::to_string(result + current) + " ";
                    }
                    curstring += word + " ";
                    result = 0;
                    current = 0;
                    onnumber = false;
                } else {
                    long long scale = num_it->second.first;
                    long long increment = num_it->second.second;
                    if (scale == 0) scale = 1; // not necessary but safe
                    current = current * scale + increment;
                    if (scale > 100) {
                        result += current;
                        current = 0;
                    }
                    onnumber = true;
                }
            }
        }

        if (onnumber) {
            curstring += std::to_string(result + current);
        }

        return curstring;
    }

    bool is_valid_input(const std::string& textnum) {
        std::string processed = textnum;
        std::replace(processed.begin(), processed.end(), '-', ' ');

        std::istringstream iss(processed);
        std::string word;
        while (iss >> word) {
            if (ordinal_words.find(word) != ordinal_words.end()) {
                continue;
            }
            std::string modified = word;
            for (const auto& ending : ordinal_endings) {
                if (modified.size() >= ending.first.size() &&
                    modified.substr(modified.size() - ending.first.size()) == ending.first) {
                    modified = modified.substr(0, modified.size() - ending.first.size()) + ending.second;
                    break;
                }
            }
            if (numwords.find(modified) == numwords.end()) {
                return false;
            }
        }
        return true;
    }
};