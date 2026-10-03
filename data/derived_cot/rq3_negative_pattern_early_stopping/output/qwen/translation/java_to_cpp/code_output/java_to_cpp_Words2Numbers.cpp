#include <vector>
#include <map>
#include <string>
#include <cctype>
#include <cmath>
#include <sstream>
#include <iostream>
#include <algorithm>

class Words2Numbers {
private:
    std::map<std::string, std::pair<int, int>> numwords;
    std::vector<std::string> units;
    std::vector<std::string> tens;
    std::vector<std::string> scales;
    std::map<std::string, int> ordinalWords;
    std::vector<std::vector<std::string>> ordinalEndings;

public:
    Words2Numbers() {
        units = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
                 "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
                 "sixteen", "seventeen", "eighteen", "nineteen"};
        tens = {"", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"};
        scales = {"hundred", "thousand", "million", "billion", "trillion"};

        // Initialize numwords
        numwords["and"] = std::make_pair(1, 0);
        for (int idx = 0; idx < units.size(); idx++) {
            numwords[units[idx]] = std::make_pair(1, idx);
        }
        for (int idx = 0; idx < tens.size(); idx++) {
            numwords[tens[idx]] = std::make_pair(1, idx * 10);
        }
        for (int idx = 0; idx < scales.size(); idx++) {
            int power = static_cast<int>(std::pow(10, (idx * 3 == 0 ? 2 : idx * 3)));
            numwords[scales[idx]] = std::make_pair(power, 0);
        }

        // Initialize ordinalWords
        ordinalWords["first"] = 1;
        ordinalWords["second"] = 2;
        ordinalWords["third"] = 3;
        ordinalWords["fifth"] = 5;
        ordinalWords["eighth"] = 8;
        ordinalWords["ninth"] = 9;
        ordinalWords["twelfth"] = 12;

        // Initialize ordinalEndings
        ordinalEndings = {{"ieth", "y"}, {"th", ""}};
    }

    std::string text2int(const std::string& textnum) {
        // Replace hyphens with spaces
        std::string text = textnum;
        for (char& c : text) {
            if (c == '-') {
                c = ' ';
            }
        }

        int current = 0, result = 0;
        std::string curstring;
        bool onnumber = false;

        // Split the string by spaces
        std::istringstream iss(text);
        std::string word;
        while (iss >> word) {
            if (ordinalWords.find(word) != ordinalWords.end()) {
                int scale = 1;
                int increment = ordinalWords[word];
                current = current * scale + increment;
                onnumber = true;
            } else {
                // Try to remove ordinal endings
                for (const auto& ending : ordinalEndings) {
                    if (word.size() > ending[0].size() && 
                        word.substr(word.size() - ending[0].size()) == ending[0]) {
                        word = word.substr(0, word.size() - ending[0].size()) + ending[1];
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
                    int scale = numwords[word].first;
                    int increment = numwords[word].second;
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

    bool isValidInput(const std::string& textnum) {
        // Replace hyphens with spaces
        std::string text = textnum;
        for (char& c : text) {
            if (c == '-') {
                c = ' ';
            }
        }

        std::istringstream iss(text);
        std::string word;
        while (iss >> word) {
            if (ordinalWords.find(word) != ordinalWords.end()) {
                continue;
            } else {
                // Try to remove ordinal endings
                for (const auto& ending : ordinalEndings) {
                    if (word.size() > ending[0].size() && 
                        word.substr(word.size() - ending[0].size()) == ending[0]) {
                        word = word.substr(0, word.size() - ending[0].size()) + ending[1];
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