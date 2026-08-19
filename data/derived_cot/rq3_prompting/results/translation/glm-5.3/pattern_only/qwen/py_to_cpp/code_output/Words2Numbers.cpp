#include <sstream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

class Words2Numbers {
public:
    Words2Numbers() {
        numwords["and"] = {1, 0};

        const std::vector<std::string> units = {
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
        };
        const std::vector<std::string> tens = {
            "", "", "twenty", "thirty", "forty", "fifty",
            "sixty", "seventy", "eighty", "ninety",
        };
        const std::vector<std::string> scales = {
            "hundred", "thousand", "million", "billion", "trillion",
        };

        for (std::size_t idx = 0; idx < units.size(); ++idx)
            numwords[units[idx]] = {1, static_cast<long long>(idx)};
        for (std::size_t idx = 0; idx < tens.size(); ++idx)
            numwords[tens[idx]] = {1, static_cast<long long>(idx) * 10};
        for (std::size_t idx = 0; idx < scales.size(); ++idx) {
            // Python: 10 ** (idx * 3 or 2)  ->  idx == 0 gives 10**2, else 10**(idx*3)
            long long exponent = (idx * 3 != 0) ? static_cast<long long>(idx) * 3 : 2;
            long long scale = 1;
            for (long long i = 0; i < exponent; ++i) scale *= 10;
            numwords[scales[idx]] = {scale, 0};
        }

        ordinal_words = {
            {"first", 1}, {"second", 2}, {"third", 3}, {"fifth", 5},
            {"eighth", 8}, {"ninth", 9}, {"twelfth", 12},
        };
        ordinal_endings = {{"ieth", "y"}, {"th", ""}};
    }

    std::string text2int(const std::string& textnum) {
        std::string normalized = replaceHyphens(textnum);

        long long current = 0;
        long long result = 0;
        std::string curstring;
        bool onnumber = false;

        std::istringstream iss(normalized);
        std::string word;
        while (iss >> word) {
            auto ordIt = ordinal_words.find(word);
            if (ordIt != ordinal_words.end()) {
                long long scale = 1;
                long long increment = ordIt->second;
                current = current * scale + increment;
                onnumber = true;
            } else {
                applyOrdinalEndings(word);

                auto it = numwords.find(word);
                if (it == numwords.end()) {
                    if (onnumber)
                        curstring += std::to_string(result + current) + " ";
                    curstring += word + " ";
                    result = current = 0;
                    onnumber = false;
                } else {
                    long long scale = it->second.first;
                    long long increment = it->second.second;
                    current = current * scale + increment;
                    if (scale > 100) {
                        result += current;
                        current = 0;
                    }
                    onnumber = true;
                }
            }
        }

        if (onnumber)
            curstring += std::to_string(result + current);

        return curstring;
    }

    bool is_valid_input(const std::string& textnum) {
        std::string normalized = replaceHyphens(textnum);

        std::istringstream iss(normalized);
        std::string word;
        while (iss >> word) {
            if (ordinal_words.find(word) != ordinal_words.end())
                continue;
            applyOrdinalEndings(word);
            if (numwords.find(word) == numwords.end())
                return false;
        }
        return true;
    }

private:
    std::unordered_map<std::string, std::pair<long long, long long>> numwords;
    std::unordered_map<std::string, long long> ordinal_words;
    std::vector<std::pair<std::string, std::string>> ordinal_endings;

    static std::string replaceHyphens(const std::string& s) {
        std::string out = s;
        for (char& c : out)
            if (c == '-') c = ' ';
        return out;
    }

    void applyOrdinalEndings(std::string& word) const {
        for (const auto& er : ordinal_endings) {
            const std::string& ending = er.first;
            const std::string& replacement = er.second;
            if (endsWith(word, ending))
                word = word.substr(0, word.size() - ending.size()) + replacement;
        }
    }

    static bool endsWith(const std::string& s, const std::string& suffix) {
        return s.size() >= suffix.size() &&
               s.compare(s.size() - suffix.size(), suffix.size(), suffix) == 0;
    }
};