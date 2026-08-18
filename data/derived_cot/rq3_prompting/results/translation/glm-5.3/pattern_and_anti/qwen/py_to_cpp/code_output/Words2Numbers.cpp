#include <algorithm>
#include <cstddef>
#include <sstream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

class Words2Numbers {
private:
    // Arbitrary-precision non-negative integer, mirroring Python's int semantics
    // (values can exceed 64-bit range, e.g. repeated "hundred"/"trillion").
    struct Big {
        std::vector<int> d;  // little-endian decimal digits; empty vector == 0

        std::string str() const {
            if (d.empty()) return "0";
            std::string s;
            s.reserve(d.size());
            for (std::size_t i = d.size(); i-- > 0;)
                s += static_cast<char>('0' + d[i]);
            return s;
        }

        void mulPow10(int k) {                 // multiply by 10^k (scale values are powers of 10)
            if (!d.empty()) d.insert(d.begin(), k, 0);
        }

        void addSmall(long long v) {           // add a small non-negative value
            std::size_t i = 0;
            while (v > 0) {
                if (i == d.size()) d.push_back(0);
                v += d[i];
                d[i] = static_cast<int>(v % 10);
                v /= 10;
                ++i;
            }
        }

        void addBig(const Big& o) {
            if (o.d.empty()) return;
            d.resize(std::max(d.size(), o.d.size()), 0);
            int carry = 0;
            for (std::size_t i = 0; i < d.size(); ++i) {
                int s = d[i] + (i < o.d.size() ? o.d[i] : 0) + carry;
                d[i] = s % 10;
                carry = s / 10;
            }
            if (carry) d.push_back(carry);
        }
    };

    struct Entry {
        int exp10;       // scale == 10^exp10  (first element of the Python tuple)
        long long inc;   // increment          (second element of the Python tuple)
    };

    std::unordered_map<std::string, Entry> numwords;
    std::unordered_map<std::string, long long> ordinal_words;
    std::vector<std::pair<std::string, std::string>> ordinal_endings;

    static std::string replaceDash(const std::string& s) {
        std::string r = s;
        for (char& c : r)
            if (c == '-') c = ' ';
        return r;
    }

    static bool endsWith(const std::string& s, const std::string& suf) {
        return s.size() >= suf.size() &&
               s.compare(s.size() - suf.size(), suf.size(), suf) == 0;
    }

public:
    Words2Numbers() {
        const char* units[] = {
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen"};
        const char* tens[] = {
            "", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty",
            "ninety"};
        const char* scales[] = {"hundred", "thousand", "million", "billion", "trillion"};

        numwords["and"] = Entry{0, 0};
        for (int i = 0; i < 20; ++i) numwords[units[i]] = Entry{0, i};
        for (int i = 0; i < 10; ++i) numwords[tens[i]] = Entry{0, static_cast<long long>(i) * 10};
        // Python: 10 ** (idx * 3 or 2) -> idx == 0 gives exponent 2, else 3*idx.
        // Note "" (from tens) stays a valid key, matching Python's dict.
        for (int i = 0; i < 5; ++i) numwords[scales[i]] = Entry{i == 0 ? 2 : 3 * i, 0};

        ordinal_words = {{"first", 1}, {"second", 2}, {"third", 3},
                         {"fifth", 5}, {"eighth", 8}, {"ninth", 9},
                         {"twelfth", 12}};
        ordinal_endings = {{"ieth", "y"}, {"th", ""}};
    }

    std::string text2int(const std::string& textnum) const {
        std::string spaced = replaceDash(textnum);

        Big current, result;   // current = result = 0
        std::string curstring;
        bool onnumber = false;

        std::istringstream iss(spaced);
        std::string word;
        while (iss >> word) {  // matches str.split() on runs of whitespace
            auto ow = ordinal_words.find(word);
            if (ow != ordinal_words.end()) {
                // scale, increment = (1, ordinal_words[word])
                current.mulPow10(0);           // current * 1
                current.addSmall(ow->second);  // + increment
                onnumber = true;
            } else {
                for (const auto& er : ordinal_endings) {
                    if (endsWith(word, er.first)) {
                        word = word.substr(0, word.size() - er.first.size()) + er.second;
                    }
                }

                auto it = numwords.find(word);
                if (it == numwords.end()) {
                    if (onnumber) {
                        Big total = result;
                        total.addBig(current);
                        curstring += total.str();   // repr(result + current)
                        curstring += ' ';
                    }
                    curstring += word;
                    curstring += ' ';
                    result = Big();   // result = current = 0
                    current = Big();
                    onnumber = false;
                } else {
                    current.mulPow10(it->second.exp10);  // current * scale
                    current.addSmall(it->second.inc);    // + increment
                    if (it->second.exp10 > 2) {          // scale > 100
                        result.addBig(current);
                        current = Big();
                    }
                    onnumber = true;
                }
            }
        }

        if (onnumber) {
            Big total = result;
            total.addBig(current);
            curstring += total.str();
        }
        return curstring;
    }

    bool is_valid_input(const std::string& textnum) const {
        std::string spaced = replaceDash(textnum);

        std::istringstream iss(spaced);
        std::string word;
        while (iss >> word) {
            if (ordinal_words.find(word) != ordinal_words.end()) continue;
            for (const auto& er : ordinal_endings) {
                if (endsWith(word, er.first)) {
                    word = word.substr(0, word.size() - er.first.size()) + er.second;
                }
            }
            if (numwords.find(word) == numwords.end()) return false;
        }
        return true;
    }
};