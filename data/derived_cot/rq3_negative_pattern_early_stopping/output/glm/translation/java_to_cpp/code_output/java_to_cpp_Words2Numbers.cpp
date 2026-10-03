#include <string>
#include <unordered_map>
#include <vector>
#include <sstream>
#include <cmath>
#include <algorithm>
#include <array>

class Words2Numbers {
private:
    std::unordered_map<std::string, std::array<int, 2>> numwords;
    std::vector<std::string> units;
    std::vector<std::string> tens;
    std::vector<std::string> scales;
    std::unordered_map<std::string, int> ordinalWords;
    std::vector<std::array<std::string, 2>> ordinalEndings;

    static bool endsWith(const std::string& str, const std::string& suffix) {
        if (suffix.size() > str.size()) return false;
        return str.compare(str.size() - suffix.size(), suffix.size(), suffix) == 0;
    }

    static std::vector<std::string> split(const std::string& s, char delim) {
        std::vector<std::string> tokens;
        std::string token;
        std::istringstream tokenStream(s);
        while (std::getline(tokenStream, token, delim)) {
            tokens.push_back(token);
        }
        while (!tokens.empty() && tokens.back().empty()) {
            tokens.pop_back();
        }
        return tokens;
    }

public:
    Words2Numbers() {
        units = {
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen"
        };
        tens = {
            "", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"
        };
        scales = {
            "hundred", "thousand", "million", "billion", "trillion"
        };

        numwords["and"] = {1, 0};
        for (int idx = 0; idx < (int)units.size(); idx++) {
            numwords[units[idx]] = {1, idx};
        }
        for (int idx = 0; idx < (int)tens.size(); idx++) {
            numwords[tens[idx]] = {1, idx * 10};
        }
        for (int idx = 0; idx < (int)scales.size(); idx++) {
            int exp = (idx * 3 == 0 ? 2 : idx * 3);
            numwords[scales[idx]] = {(int)std::pow(10, exp), 0};
        }

        ordinalWords["first"] = 1;
        ordinalWords["second"] = 2;
        ordinalWords["third"] = 3;
        ordinalWords["fifth"] = 5;
        ordinalWords["eighth"] = 8;
        ordinalWords["ninth"] = 9;
        ordinalWords["twelfth"] = 12;

        ordinalEndings = {
            {"ieth", "y"}, {"th", ""}
        };
    }

    std::string text2int(std::string textnum) {
        std::replace(textnum.begin(), textnum.end(), '-', ' ');

        int current = 0, result = 0;
        std::stringstream curstring;
        bool onnumber = false;

        for (const std::string& wordOrig : split(textnum, ' ')) {
            std::string word = wordOrig;
            if (ordinalWords.count(word)) {
                int scale = 1, increment = ordinalWords[word];
                current = current * scale + increment;
                onnumber = true;
            } else {
                for (const auto& ending : ordinalEndings) {
                    if (endsWith(word, ending[0])) {
                        word = word.substr(0, word.length() - ending[0].length()) + ending[1];
                    }
                }

                if (!numwords.count(word)) {
                    if (onnumber) {
                        curstring << (result + current) << " ";
                    }
                    curstring << word << " ";
                    result = current = 0;
                    onnumber = false;
                } else {
                    int scale = numwords[word][0];
                    int increment = numwords[word][1];
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
        std::replace(textnum.begin(), textnum.end(), '-', ' ');

        for (const std::string& wordOrig : split(textnum, ' ')) {
            std::string word = wordOrig;
            if (ordinalWords.count(word)) {
                continue;
            } else {
                for (const auto& ending : ordinalEndings) {
                    if (endsWith(word, ending[0])) {
                        word = word.substr(0, word.length() - ending[0].length()) + ending[1];
                    }
                }

                if (!numwords.count(word)) {
                    return false;
                }
            }
        }

        return true;
    }
};