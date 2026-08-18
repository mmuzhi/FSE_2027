#include <string>
#include <vector>
#include <map>
#include <utility>

namespace org {
namespace example {

class Words2Numbers {
private:
    std::map<std::string, std::pair<int, int> > numwords;
    std::vector<std::string> units;
    std::vector<std::string> tens;
    std::vector<std::string> scales;
    std::map<std::string, int> ordinalWords;
    std::vector<std::pair<std::string, std::string> > ordinalEndings;

    static bool endsWith(const std::string& s, const std::string& suffix) {
        return s.size() >= suffix.size() &&
               s.compare(s.size() - suffix.size(), suffix.size(), suffix) == 0;
    }

    // Mimics Java's String.split(" "): split on each single space, keeping
    // interior empty tokens but dropping trailing empty tokens. If no space
    // occurs at all, the whole string is the single token (even if empty).
    static std::vector<std::string> splitOnSingleSpace(const std::string& s) {
        std::vector<std::string> tokens;
        std::string cur;
        bool sawSpace = false;
        for (std::string::size_type i = 0; i < s.size(); ++i) {
            if (s[i] == ' ') {
                sawSpace = true;
                tokens.push_back(cur);
                cur.clear();
            } else {
                cur += s[i];
            }
        }
        tokens.push_back(cur);
        if (sawSpace) {
            while (!tokens.empty() && tokens.back().empty()) tokens.pop_back();
        }
        return tokens;
    }

    // Java int arithmetic wraps on overflow; emulate via unsigned to keep
    // identical results without signed-overflow UB in C++.
    static int wrapMulAdd(int a, int b, int c) {
        return static_cast<int>(static_cast<unsigned int>(a) * static_cast<unsigned int>(b) +
                                static_cast<unsigned int>(c));
    }

    static int wrapAdd(int a, int b) {
        return static_cast<int>(static_cast<unsigned int>(a) + static_cast<unsigned int>(b));
    }

public:
    Words2Numbers() {
        units = std::vector<std::string>{
                "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
                "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
                "sixteen", "seventeen", "eighteen", "nineteen"
        };
        tens = std::vector<std::string>{
                "", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"
        };
        scales = std::vector<std::string>{
                "hundred", "thousand", "million", "billion", "trillion"
        };

        numwords["and"] = std::make_pair(1, 0);
        for (std::size_t idx = 0; idx < units.size(); ++idx) {
            numwords[units[idx]] = std::make_pair(1, static_cast<int>(idx));
        }
        for (std::size_t idx = 0; idx < tens.size(); ++idx) {
            numwords[tens[idx]] = std::make_pair(1, static_cast<int>(idx * 10));
        }
        for (std::size_t idx = 0; idx < scales.size(); ++idx) {
            int e = (idx * 3 == 0) ? 2 : static_cast<int>(idx * 3);
            unsigned long long p = 1;
            for (int i = 0; i < e; ++i) p *= 10ULL;
            // equivalent of (int) Math.pow(10, e), including Java's wrap for 10^12
            int scale = static_cast<int>(static_cast<unsigned int>(p));
            numwords[scales[idx]] = std::make_pair(scale, 0);
        }

        ordinalWords["first"] = 1;
        ordinalWords["second"] = 2;
        ordinalWords["third"] = 3;
        ordinalWords["fifth"] = 5;
        ordinalWords["eighth"] = 8;
        ordinalWords["ninth"] = 9;
        ordinalWords["twelfth"] = 12;

        ordinalEndings.push_back(std::make_pair("ieth", "y"));
        ordinalEndings.push_back(std::make_pair("th", ""));
    }

    std::string text2int(std::string textnum) {
        for (std::string::size_type i = 0; i < textnum.size(); ++i) {
            if (textnum[i] == '-') textnum[i] = ' ';
        }

        int current = 0, result = 0;
        std::string curstring;
        bool onnumber = false;

        for (const std::string& tok : splitOnSingleSpace(textnum)) {
            std::string word = tok;
            std::map<std::string, int>::const_iterator ow = ordinalWords.find(word);
            if (ow != ordinalWords.end()) {
                int scale = 1;
                int increment = ow->second;
                current = wrapMulAdd(current, scale, increment);
                onnumber = true;
            } else {
                for (const std::pair<std::string, std::string>& ending : ordinalEndings) {
                    if (endsWith(word, ending.first)) {
                        word = word.substr(0, word.size() - ending.first.size()) + ending.second;
                    }
                }

                std::map<std::string, std::pair<int, int> >::const_iterator nw = numwords.find(word);
                if (nw == numwords.end()) {
                    if (onnumber) {
                        curstring += std::to_string(wrapAdd(result, current));
                        curstring += " ";
                    }
                    curstring += word;
                    curstring += " ";
                    result = current = 0;
                    onnumber = false;
                } else {
                    int scale = nw->second.first;
                    int increment = nw->second.second;
                    current = wrapMulAdd(current, scale, increment);
                    if (scale > 100) {
                        result = wrapAdd(result, current);
                        current = 0;
                    }
                    onnumber = true;
                }
            }
        }

        if (onnumber) {
            curstring += std::to_string(wrapAdd(result, current));
        }

        return curstring;
    }

    bool isValidInput(std::string textnum) {
        for (std::string::size_type i = 0; i < textnum.size(); ++i) {
            if (textnum[i] == '-') textnum[i] = ' ';
        }

        for (const std::string& tok : splitOnSingleSpace(textnum)) {
            std::string word = tok;
            if (ordinalWords.count(word) > 0) {
                continue;
            } else {
                for (const std::pair<std::string, std::string>& ending : ordinalEndings) {
                    if (endsWith(word, ending.first)) {
                        word = word.substr(0, word.size() - ending.first.size()) + ending.second;
                    }
                }

                if (numwords.count(word) == 0) {
                    return false;
                }
            }
        }

        return true;
    }
};

} // namespace example
} // namespace org