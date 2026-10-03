#include <string>
#include <vector>
#include <unordered_map>
#include <sstream>
#include <algorithm>

class Words2Numbers {
private:
    std::unordered_map<std::string, std::pair<long long, long long>> numwords;
    std::vector<std::string> units;
    std::vector<std::string> tens;
    std::vector<std::string> scales;
    std::unordered_map<std::string, int> ordinal_words;
    std::vector<std::pair<std::string, std::string>> ordinal_endings;

public:
    Words2Numbers() {
        units = {
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen"
        };
        tens = {"", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"};
        scales = {"hundred", "thousand", "million", "billion", "trillion"};

        numwords["and"] = {1, 0};
        for (int idx = 0; idx < units.size(); ++idx) {
            numwords[units[idx]] = {1, idx};
        }
        for (int idx = 0; idx < tens.size(); ++idx) {
            numwords[tens[idx]] = {1, idx * 10};
        }
        long long scale_vals[] = {100, 1000, 1000000, 1000000000, 1000000000000};
        for (int idx = 0; idx < scales.size(); ++idx) {
            numwords[scales[idx]] = {scale_vals[idx], 0};
        }

        ordinal_words = {{"first", 1}, {"second", 2}, {"third", 3}, {"fifth", 5}, {"eighth", 8}, {"ninth", 9}, {"twelfth", 12}};
        ordinal_endings = {{"ieth", "y"}, {"th", ""}};
    }

    std::string text2int(std::string textnum) {
        std::replace(textnum.begin(), textnum.end(), '-', ' ');

        long long current = 0, result = 0;
        std::string curstring = "";
        bool onnumber = false;

        std::stringstream ss(textnum);
        std::string word;
        while (ss >> word) {
            if (ordinal_words.count(word)) {
                long long scale = 1;
                long long increment = ordinal_words[word];
                current = current * scale + increment;
                onnumber = true;
            } else {
                for (const auto& p : ordinal_endings) {
                    const std::string& ending = p.first;
                    const std::string& replacement = p.second;
                    if (ending.empty()) {
                        word = "";
                    } else if (word.size() >= ending.size() && word.compare(word.size() - ending.size(), ending.size(), ending) == 0) {
                        word = word.substr(0, word.size() - ending.size()) + replacement;
                    }
                }

                if (numwords.find(word) == numwords.end()) {
                    if (onnumber) {
                        curstring += std::to_string(result + current) + " ";
                    }
                    curstring += word + " ";
                    result = current = 0;
                    onnumber = false;
                } else {
                    long long scale = numwords[word].first;
                    long long increment = numwords[word].second;
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

    bool is_valid_input(std::string textnum) {
        std::replace(textnum.begin(), textnum.end(), '-', ' ');

        std::stringstream ss(textnum);
        std::string word;
        while (ss >> word) {
            if (ordinal_words.count(word)) {
                continue;
            } else {
                for (const auto& p : ordinal_endings) {
                    const std::string& ending = p.first;
                    const std::string& replacement = p.second;
                    if (ending.empty()) {
                        word = "";
                    } else if (word.size() >= ending.size() && word.compare(word.size() - ending.size(), ending.size(), ending) == 0) {
                        word = word.substr(0, word.size() - ending.size()) + replacement;
                    }
                }

                if (numwords.find(word) == numwords.end()) {
                    return false;
                }
            }
        }

        return true;
    }
};