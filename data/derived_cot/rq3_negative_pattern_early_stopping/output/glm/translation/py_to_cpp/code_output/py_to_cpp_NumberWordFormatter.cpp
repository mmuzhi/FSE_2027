#include <string>
#include <vector>
#include <algorithm>
#include <sstream>

class NumberWordFormatter {
private:
    std::vector<std::string> NUMBER = {"", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"};
    std::vector<std::string> NUMBER_TEEN = {"TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN"};
    std::vector<std::string> NUMBER_TEN = {"TEN", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"};
    std::vector<std::string> NUMBER_MORE = {"", "THOUSAND", "MILLION", "BILLION"};
    std::vector<std::string> NUMBER_SUFFIX = {"k", "w", "", "m", "", "", "b", "", "", "t", "", "", "p", "", "", "e"};

    std::string trim(const std::string& str) {
        size_t first = str.find_first_not_of(' ');
        if (std::string::npos == first) {
            return "";
        }
        size_t last = str.find_last_not_of(' ');
        return str.substr(first, (last - first + 1));
    }

public:
    std::string format(std::nullptr_t) {
        return "";
    }

    std::string format(int x) {
        return format_string(std::to_string(x));
    }

    std::string format(long long x) {
        return format_string(std::to_string(x));
    }

    std::string format(double x) {
        return format_string(std::to_string(x));
    }

    std::string format_string(std::string x) {
        std::string lstr, rstr;
        size_t dot_pos = x.find('.');
        if (dot_pos == std::string::npos) {
            lstr = x;
            rstr = "";
        } else {
            lstr = x.substr(0, dot_pos);
            rstr = x.substr(dot_pos + 1);
        }

        std::string lstrrev = lstr;
        std::reverse(lstrrev.begin(), lstrrev.end());

        if (lstrrev.length() % 3 == 1) {
            lstrrev += "00";
        } else if (lstrrev.length() % 3 == 2) {
            lstrrev += "0";
        }

        std::string lm = "";

        for (size_t i = 0; i < lstrrev.length() / 3; ++i) {
            std::string chunk = lstrrev.substr(3 * i, 3);
            std::reverse(chunk.begin(), chunk.end());

            if (chunk != "000") {
                lm = trans_three(chunk) + " " + parse_more(i) + " " + lm;
            } else {
                lm += trans_three(chunk);
            }
        }

        std::string xs = "";
        if (!rstr.empty()) {
            xs = "AND CENTS " + trans_two(rstr) + " ";
        }

        std::string lm_stripped = trim(lm);
        if (lm_stripped.empty()) {
            return "ZERO ONLY";
        } else {
            return lm_stripped + " " + xs + "ONLY";
        }
    }

    std::string trans_two(std::string s) {
        if (s.length() < 2) {
            s = std::string(2 - s.length(), '0') + s;
        }
        if (s[0] == '0') {
            return NUMBER[s[1] - '0'];
        } else if (s[0] == '1') {
            return NUMBER_TEEN[std::stoi(s) - 10];
        } else if (s[1] == '0') {
            return NUMBER_TEN[s[0] - '0' - 1];
        } else {
            return NUMBER_TEN[s[0] - '0' - 1] + " " + NUMBER[s[1] - '0'];
        }
    }

    std::string trans_three(std::string s) {
        if (s[0] == '0') {
            return trans_two(s.substr(1));
        } else if (s.substr(1) == "00") {
            return NUMBER[s[0] - '0'] + " HUNDRED";
        } else {
            return NUMBER[s[0] - '0'] + " HUNDRED AND " + trans_two(s.substr(1));
        }
    }

    std::string parse_more(int i) {
        return NUMBER_MORE.at(i);
    }
};