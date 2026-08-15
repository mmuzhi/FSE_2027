#include <string>
#include <vector>
#include <unordered_map>
#include <utility>
#include <cstdint>

using namespace std;

class Words2Numbers {
private:
    unordered_map<string, pair<int32_t, int32_t>> numwords;
    vector<string> units;
    vector<string> tens;
    vector<string> scales;
    unordered_map<string, int32_t> ordinalWords;
    vector<pair<string, string>> ordinalEndings;

    static bool endsWith(const string& str, const string& suffix) {
        if (str.size() < suffix.size()) return false;
        return str.compare(str.size() - suffix.size(), suffix.size(), suffix) == 0;
    }

    static vector<string> splitOnSpaces(const string& s) {
        vector<string> result;
        if (s.empty()) {
            result.push_back("");
            return result;
        }
        string cur;
        for (char c : s) {
            if (c == ' ') {
                result.push_back(cur);
                cur.clear();
            } else {
                cur.push_back(c);
            }
        }
        result.push_back(cur);
        while (!result.empty() && result.back().empty()) {
            result.pop_back();
        }
        return result;
    }

    static int32_t add32(int32_t a, int32_t b) {
        return (int32_t)((uint32_t)a + (uint32_t)b);
    }

    static int32_t mulAdd32(int32_t current, int32_t scale, int32_t increment) {
        return (int32_t)((uint32_t)current * (uint32_t)scale + (uint32_t)increment);
    }

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
        for (int idx = 0; idx < (int)units.size(); idx++) {
            numwords[units[idx]] = {1, idx};
        }
        for (int idx = 0; idx < (int)tens.size(); idx++) {
            numwords[tens[idx]] = {1, idx * 10};
        }
        for (int idx = 0; idx < (int)scales.size(); idx++) {
            int32_t scale;
            if (idx == 0) {
                scale = 100;
            } else {
                int64_t p = 1;
                for (int j = 0; j < idx * 3; j++) {
                    p *= 10;
                }
                scale = (p > INT32_MAX) ? INT32_MAX : (int32_t)p;
            }
            numwords[scales[idx]] = {scale, 0};
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

    string text2int(string textnum) {
        for (size_t i = 0; i < textnum.size(); i++) {
            if (textnum[i] == '-') textnum[i] = ' ';
        }

        int32_t current = 0, result = 0;
        string curstring;
        bool onnumber = false;

        vector<string> words = splitOnSpaces(textnum);
        for (string word : words) {
            auto ordIt = ordinalWords.find(word);
            if (ordIt != ordinalWords.end()) {
                int32_t scale = 1;
                int32_t increment = ordIt->second;
                current = mulAdd32(current, scale, increment);
                onnumber = true;
            } else {
                for (const auto& ending : ordinalEndings) {
                    if (endsWith(word, ending.first)) {
                        word = word.substr(0, word.size() - ending.first.size()) + ending.second;
                    }
                }

                auto numIt = numwords.find(word);
                if (numIt == numwords.end()) {
                    if (onnumber) {
                        curstring += to_string(add32(result, current));
                        curstring += " ";
                    }
                    curstring += word;
                    curstring += " ";
                    result = current = 0;
                    onnumber = false;
                } else {
                    int32_t scale = numIt->second.first;
                    int32_t increment = numIt->second.second;
                    current = mulAdd32(current, scale, increment);
                    if (scale > 100) {
                        result = add32(result, current);
                        current = 0;
                    }
                    onnumber = true;
                }
            }
        }

        if (onnumber) {
            curstring += to_string(add32(result, current));
        }

        return curstring;
    }

    bool isValidInput(string textnum) {
        for (size_t i = 0; i < textnum.size(); i++) {
            if (textnum[i] == '-') textnum[i] = ' ';
        }

        vector<string> words = splitOnSpaces(textnum);
        for (string word : words) {
            if (ordinalWords.find(word) != ordinalWords.end()) {
                continue;
            } else {
                for (const auto& ending : ordinalEndings) {
                    if (endsWith(word, ending.first)) {
                        word = word.substr(0, word.size() - ending.first.size()) + ending.second;
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