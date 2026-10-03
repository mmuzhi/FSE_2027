#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>
#include <cmath>
#include <utility>

class Words2Numbers {
private:
    std::unordered_map<std::string, std::pair<int, int>> numwords;
    std::vector<std::string> units;
    std::vector<std::string> tens;
    std::vector<std::string> scales;
    std::unordered_map<std::string, int> ordinalWords;
    std::vector<std::pair<std::string, std::string>> ordinalEndings;

    std::vector<std::string> splitString(const std::string& s) {
        std::vector<std::string> tokens;
        std::size_t start = 0;
        while (start <= s.length()) {
            std::size_t end = s.find(' ', start);
            if (end == std::string::npos) {
                tokens.push_back(s.substr(start));
                break;
            } else {
                tokens.push_back(s.substr(start, end - start));
                start = end + 1;
            }
        }
        return tokens;
    }

public:
    Words2Numbers() {
        units = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
                 "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
                 "sixteen", "seventeen", "eighteen", "nineteen"};
        tens = {"", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"};
        scales = {"hundred", "thousand", "million", "billion", "trillion"};

        numwords["and"] = {1, 0};
        for (std::size_t i = 0; i < units.size(); ++i) {
            numwords[units[i]] = {1, static_cast<int>(i)};
        }
        for (std::size_t i = 0; i < tens.size(); ++i) {
            numwords[tens[i]] = {1, static_cast<int>(i) * 10};
        }
        for (std::size_t i = 0; i < scales.size(); ++i) {
            int scale = (i * 3 == 0) ? 100 : static_cast<int>(std::pow(10.0, i * 3));
            numwords[scales[i]] = {scale, 0};
        }

        ordinalWords["first"] = 1;
        ordinalWords["second"] = 2;
        ordinalWords["third"] = 3;
        ordinalWords["fifth"] = 5;
        ordinalWords["eighth"] = 8;
        ordinalWords["ninth"] = 9;
        ordinalWords["twelfth"] = 12;

        ordinalEndings = {{"ieth", "y"}, {"th", ""}};
    }

    std::string text2int(std::string textnum) {
        for (auto& ch : textnum) {
            if (ch == '-') ch = ' ';
        }

        int current = 0, result = 0;
        std::ostringstream curstring;
        bool onnumber = false;

        std::vector<std::string> words = splitString(textnum);
        for (const std::string& word : words) {
            std::string w = word;
            if (ordinalWords.count(w)) {
                int scale = 1;
                int increment = ordinalWords.at(w);
                current = current * scale + increment;
                onnumber = true;
            } else {
                for (const auto& ending : ordinalEndings) {
                    if (w.size() >= ending.first.size() &&
                        w.rfind(ending.first) == w.size() - ending.first.size()) {
                        w = w.substr(0, w.size() - ending.first.size()) + ending.second;
                    }
                }

                if (!numwords.count(w)) {
                    if (onnumber) {
                        curstring << (result + current) << " ";
                    }
                    curstring << word << " ";
                    result = 0;
                    current = 0;
                    onnumber = false;
                } else {
                    int scale = numwords[w].first;
                    int increment = numwords[w].second;
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
            curstring << (result + current);
        }

        return curstring.str();
    }

    bool isValidInput(std::string textnum) {
        for (auto& ch : textnum) {
            if (ch == '-') ch = ' ';
        }

        std::vector<std::string> words = splitString(textnum);
        for (const std::string& word : words) {
            std::string w = word;
            if (ordinalWords.count(w)) {
                continue;
            } else {
                for (const auto& ending : ordinalEndings) {
                    if (w.size() >= ending.first.size() &&
                        w.rfind(ending.first) == w.size() - ending.first.size()) {
                        w = w.substr(0, w.size() - ending.first.size()) + ending.second;
                    }
                }

                if (!numwords.count(w)) {
                    return false;
                }
            }
        }
        return true;
    }
};