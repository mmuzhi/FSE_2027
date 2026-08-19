#include <string>
#include <vector>
#include <array>
#include <unordered_map>
#include <algorithm>

namespace org {
namespace example {

class Words2Numbers {
private:
    std::unordered_map<std::string, std::array<int, 2>> numwords;
    std::vector<std::string> units;
    std::vector<std::string> tens;
    std::vector<std::string> scales;
    std::unordered_map<std::string, int> ordinalWords;
    std::vector<std::array<std::string, 2>> ordinalEndings;

    static bool endsWith(const std::string& s, const std::string& suffix) {
        return s.size() >= suffix.size() &&
               s.compare(s.size() - suffix.size(), suffix.size(), suffix) == 0;
    }

    // Mimics Java's String.split(" "): keeps inner empty tokens, drops trailing empty tokens.
    static std::vector<std::string> javaSplitSpace(const std::string& s) {
        std::vector<std::string> parts;
        std::string cur;
        for (char c : s) {
            if (c == ' ') {
                parts.push_back(cur);
                cur.clear();
            } else {
                cur += c;
            }
        }
        parts.push_back(cur);
        while (!parts.empty() && parts.back().empty()) {
            parts.pop_back();
        }
        return parts;
    }

    // Mimics Java's saturating (int) cast of Math.pow(10, exp).
    static int pow10AsInt(int exp) {
        long long p = 1;
        for (int i = 0; i < exp; ++i) p *= 10;
        return (p > 2147483647LL) ? 2147483647 : (int)p;
    }

public:
    Words2Numbers() {
        units = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
                 "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
                 "sixteen", "seventeen", "eighteen", "nineteen"};
        tens = {"", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"};
        scales = {"hundred", "thousand", "million", "billion", "trillion"};

        numwords["and"] = {1, 0};
        for (int idx = 0; idx < static_cast<int>(units.size()); idx++) {
            numwords[units[idx]] = {1, idx};
        }
        // Note: the empty-string key is inserted twice (idx 0 and 1), last wins — same as Java.
        for (int idx = 0; idx < static_cast<int>(tens.size()); idx++) {
            numwords[tens[idx]] = {1, idx * 10};
        }
        for (int idx = 0; idx < static_cast<int>(scales.size()); idx++) {
            int exp = (idx * 3 == 0) ? 2 : idx * 3;
            numwords[scales[idx]] = {pow10AsInt(exp), 0};
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
        std::replace(textnum.begin(), textnum.end(), '-', ' ');

        int current = 0, result = 0;
        std::string curstring;
        bool onnumber = false;

        for (std::string word : javaSplitSpace(textnum)) {
            if (ordinalWords.find(word) != ordinalWords.end()) {
                int scale = 1;
                int increment = ordinalWords[word];
                current = (int)((unsigned)current * (unsigned)scale + (unsigned)increment);
                onnumber = true;
            } else {
                for (const auto& ending : ordinalEndings) {
                    if (endsWith(word, ending[0])) {
                        word = word.substr(0, word.size() - ending[0].size()) + ending[1];
                    }
                }

                auto it = numwords.find(word);
                if (it == numwords.end()) {
                    if (onnumber) {
                        curstring += std::to_string((int)((unsigned)result + (unsigned)current));
                        curstring += " ";
                    }
                    curstring += word;
                    curstring += " ";
                    result = current = 0;
                    onnumber = false;
                } else {
                    int scale = it->second[0];
                    int increment = it->second[1];
                    current = (int)((unsigned)current * (unsigned)scale + (unsigned)increment);
                    if (scale > 100) {
                        result = (int)((unsigned)result + (unsigned)current);
                        current = 0;
                    }
                    onnumber = true;
                }
            }
        }

        if (onnumber) {
            curstring += std::to_string((int)((unsigned)result + (unsigned)current));
        }

        return curstring;
    }

    bool isValidInput(std::string textnum) {
        std::replace(textnum.begin(), textnum.end(), '-', ' ');

        for (std::string word : javaSplitSpace(textnum)) {
            if (ordinalWords.find(word) != ordinalWords.end()) {
                continue;
            }
            for (const auto& ending : ordinalEndings) {
                if (endsWith(word, ending[0])) {
                    word = word.substr(0, word.size() - ending[0].size()) + ending[1];
                }
            }
            if (numwords.find(word) == numwords.end()) {
                return false;
            }
        }

        return true;
    }
};

} // namespace example
} // namespace org