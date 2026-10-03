#include <vector>
#include <map>
#include <string>
#include <sstream>
#include <cctype>
#include <algorithm>

class Words2Numbers {
public:
    Words2Numbers() {
        // Initialize units, tens, and scales
        for (int idx = 0; idx < 20; ++idx) {
            units.push_back(std::string());
            if (idx < 10) {
                units[idx] = std::string("zero").substr(0, idx) + (idx == 0 ? "" : "o") + (idx == 1 ? "ne" : (idx == 2 ? "two" : (idx == 3 ? "three" : (idx == 4 ? "four" : (idx == 5 ? "five" : (idx == 6 ? "six" : (idx == 7 ? "seven" : (idx == 8 ? "eight" : "nine"))))))));
            } else {
                units[idx] = std::to_string(idx);
            }
        }

        for (int idx = 0; idx < 10; ++idx) {
            tens.push_back(std::string());
            if (idx == 0 || idx == 1) {
                tens[idx] = std::string();
            } else {
                tens[idx] = std::string("ten") + (idx == 2 ? "ty" : (idx == 3 ? "thirty" : (idx == 4 ? "forty" : (idx == 5 ? "fifty" : (idx == 6 ? "sixty" : (idx == 7 ? "seventy" : (idx == 8 ? "eighty" : "ninety"))))))) + (idx % 10 == 0 ? "" : "s");
            }
        }

        scales = {"hundred", "thousand", "million", "billion", "trillion"};

        // Initialize numwords
        numwords["and"] = std::make_pair(1, 0);
        for (int idx = 0; idx < units.size(); ++idx) {
            numwords[units[idx]] = std::make_pair(1, idx);
        }
        for (int idx = 0; idx < tens.size(); ++idx) {
            numwords[tens[idx]] = std::make_pair(1, idx * 10);
        }
        for (int idx = 0; idx < scales.size(); ++idx) {
            int power = idx == 0 ? 2 : 3 * idx;
            int value = 1;
            for (int i = 0; i < power; ++i) {
                value *= 10;
            }
            numwords[scales[idx]] = std::make_pair(value, 0);
        }

        // Initialize ordinal_words and ordinal_endings
        ordinal_words["first"] = 1;
        ordinal_words["second"] = 2;
        ordinal_words["third"] = 3;
        ordinal_words["fifth"] = 5;
        ordinal_words["eighth"] = 8;
        ordinal_words["ninth"] = 9;
        ordinal_words["twelfth"] = 12;

        ordinal_endings.push_back(std::make_pair(std::string("ieth"), std::string("y")));
        ordinal_endings.push_back(std::make_pair(std::string("th"), ""));
    }

    std::string text2int(const std::string& textnum) {
        std::string corrected = textnum;
        size_t pos = 0;
        while ((pos = corrected.find('-', pos)) != std::string::npos) {
            corrected.replace(pos, 1, " ");
            pos++;
        }

        std::istringstream iss(corrected);
        std::vector<std::string> words;
        std::string word;
        while (iss >> word) {
            words.push_back(word);
        }

        std::string curstring;
        bool onnumber = false;
        long result = 0;
        long current = 0;

        for (const auto& w : words) {
            if (ordinal_words.find(w) != ordinal_words.end()) {
                long scale = 1;
                long increment = ordinal_words[w];
                current = current * scale + increment;
                onnumber = true;
            } else {
                std::string base = w;
                for (const auto& ending : ordinal_endings) {
                    if (base.size() > ending.first.size() && 
                        base.substr(base.size() - ending.first.size()) == ending.first) {
                        base = base.substr(0, base.size() - ending.first.size()) + ending.second;
                    }
                }

                if (numwords.find(base) == numwords.end()) {
                    if (onnumber) {
                        curstring += std::to_string(result + current) + " ";
                        onnumber = false;
                    }
                    curstring += base + " ";
                    result = current = 0;
                } else {
                    auto it = numwords.find(base);
                    long scale = it->second.first;
                    long increment = it->second.second;
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
        std::string corrected = textnum;
        size_t pos = 0;
        while ((pos = corrected.find('-', pos)) != std::string::npos) {
            corrected.replace(pos, 1, " ");
            pos++;
        }

        std::istringstream iss(corrected);
        std::vector<std::string> words;
        std::string word;
        while (iss >> word) {
            if (ordinal_words.find(word) != ordinal_words.end()) {
                continue;
            }

            std::string base = word;
            for (const auto& ending : ordinal_endings) {
                if (base.size() > ending.first.size() && 
                    base.substr(base.size() - ending.first.size()) == ending.first) {
                    base = base.substr(0, base.size() - ending.first.size()) + ending.second;
                }
            }

            if (numwords.find(base) == numwords.end()) {
                return false;
            }
        }

        return true;
    }

private:
    std::vector<std::string> units;
    std::vector<std::string> tens;
    std::vector<std::string> scales;
    std::map<std::string, std::pair<long, long>> numwords;
    std::map<std::string, long> ordinal_words;
    std::vector<std::pair<std::string, std::string>> ordinal_endings;
};