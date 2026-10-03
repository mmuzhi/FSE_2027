#include <string>
#include <vector>
#include <algorithm>
#include <cctype>

class NumberWordFormatter {
private:
    std::vector<std::string> NUMBER;
    std::vector<std::string> NUMBER_TEEN;
    std::vector<std::string> NUMBER_TEN;
    std::vector<std::string> NUMBER_MORE;
    std::vector<std::string> NUMBER_SUFFIX;

    // Trim leading and trailing spaces
    static std::string trim(const std::string& str) {
        size_t first = 0;
        while (first < str.size() && std::isspace(static_cast<unsigned char>(str[first]))) {
            ++first;
        }
        size_t last = str.size();
        while (last > first && std::isspace(static_cast<unsigned char>(str[last - 1]))) {
            --last;
        }
        return str.substr(first, last - first);
    }

    // Pad string to at least 2 characters with leading zeros
    static std::string zfill2(const std::string& s) {
        if (s.size() >= 2) return s;
        if (s.size() == 0) return "00";
        return "0" + s;
    }

public:
    NumberWordFormatter() {
        NUMBER = {"", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"};
        NUMBER_TEEN = {"TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN"};
        NUMBER_TEN = {"TEN", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"};
        NUMBER_MORE = {"", "THOUSAND", "MILLION", "BILLION"};
        NUMBER_SUFFIX = {"k", "w", "", "m", "", "", "b", "", "", "t", "", "", "p", "", "", "e"};
    }

    std::string format(int x) {
        return format_string(std::to_string(x));
    }

    std::string format(double x) {
        // Simulate Python's str(x) for integers and floats.
        // For integers (no fractional part) we output without decimal point.
        // For float with fractional part, include a decimal point but no trailing zeros.
        // This is not perfect but matches typical usage.
        long long intPart = static_cast<long long>(x);
        double fracPart = x - static_cast<double>(intPart);
        if (fracPart == 0.0) {
            return format_string(std::to_string(intPart));
        } else {
            // Convert to string with at most 10 decimal places, removing trailing zeros
            std::string s = std::to_string(x);
            // Remove trailing zeros after decimal point
            size_t dot = s.find('.');
            if (dot != std::string::npos) {
                size_t last_non_zero = s.find_last_not_of('0');
                if (last_non_zero > dot) {
                    s.erase(last_non_zero + 1);
                } else {
                    // Only zeros after decimal, remove decimal point as well
                    s.erase(dot);
                }
            }
            return format_string(s);
        }
    }

    std::string format_string(const std::string& x) {
        // Split on '.'
        std::string lstr, rstr;
        size_t dot = x.find('.');
        if (dot == std::string::npos) {
            lstr = x;
            rstr = "";
        } else {
            lstr = x.substr(0, dot);
            rstr = x.substr(dot + 1);
        }

        // Reverse integer part
        std::string lstrrev = lstr;
        std::reverse(lstrrev.begin(), lstrrev.end());

        // Pad to multiple of 3
        while (lstrrev.size() % 3 != 0) {
            lstrrev.push_back('0');
        }

        // Process groups
        std::vector<std::string> a(5);
        std::string lm = "";
        size_t groups = lstrrev.size() / 3;
        for (size_t i = 0; i < groups; ++i) {
            std::string group = lstrrev.substr(3 * i, 3);
            std::reverse(group.begin(), group.end());
            a[i] = group;
            if (a[i] != "000") {
                lm = trans_three(a[i]) + " " + parse_more(i) + " " + lm;
            } else {
                lm += trans_three(a[i]);
            }
        }

        std::string xs = "";
        if (!rstr.empty()) {
            xs = "AND CENTS " + trans_two(rstr) + " ";
        }

        std::string result = trim(lm);
        if (result.empty()) {
            return "ZERO ONLY";
        } else {
            return result + " " + xs + "ONLY";
        }
    }

    std::string trans_two(const std::string& s) {
        std::string padded = zfill2(s);
        if (padded[0] == '0') {
            return NUMBER[static_cast<size_t>(padded[1] - '0')];
        } else if (padded[0] == '1') {
            int idx = std::stoi(padded) - 10;
            return NUMBER_TEEN[static_cast<size_t>(idx)];
        } else if (padded[1] == '0') {
            return NUMBER_TEN[static_cast<size_t>(padded[0] - '1')];
        } else {
            return NUMBER_TEN[static_cast<size_t>(padded[0] - '1')] + " " + NUMBER[static_cast<size_t>(padded[1] - '0')];
        }
    }

    std::string trans_three(const std::string& s) {
        if (s[0] == '0') {
            return trans_two(s.substr(1));
        } else if (s[1] == '0' && s[2] == '0') {
            return NUMBER[static_cast<size_t>(s[0] - '0')] + " HUNDRED";
        } else {
            return NUMBER[static_cast<size_t>(s[0] - '0')] + " HUNDRED AND " + trans_two(s.substr(1));
        }
    }

    std::string parse_more(size_t i) {
        return NUMBER_MORE.at(i); // at() for bounds checking like Python IndexError
    }
};