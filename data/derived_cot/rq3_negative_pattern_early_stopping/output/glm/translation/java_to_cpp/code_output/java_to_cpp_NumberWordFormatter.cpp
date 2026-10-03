#include <string>
#include <vector>
#include <algorithm>
#include <sstream>

class NumberWordFormatter {
private:
    const std::string NUMBER[10] = {"", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"};
    const std::string NUMBER_TEEN[10] = {"TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN"};
    const std::string NUMBER_TEN[9] = {"TEN", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"};
    const std::string NUMBER_MORE[4] = {"", "THOUSAND", "MILLION", "BILLION"};
    const std::string NUMBER_SUFFIX[16] = {"k", "w", "", "m", "", "", "b", "", "", "t", "", "", "p", "", "", "e"};

    std::vector<std::string> split(const std::string& s, char delimiter) {
        std::vector<std::string> tokens;
        std::string token;
        std::istringstream tokenStream(s);
        while (std::getline(tokenStream, token, delimiter)) {
            tokens.push_back(token);
        }
        return tokens;
    }

    std::string trim(const std::string& s) {
        size_t start = s.find_first_not_of(" \t\n\r");
        if (start == std::string::npos) return "";
        size_t end = s.find_last_not_of(" \t\n\r");
        return s.substr(start, end - start + 1);
    }

public:
    std::string format(const std::string* x) {
        if (x == nullptr) {
            return "";
        }
        return formatString(*x);
    }

    std::string formatString(const std::string& x) {
        std::vector<std::string> parts = split(x, '.');
        std::string lstr = parts[0];
        std::string rstr = parts.size() > 1 ? parts[1] : "";

        std::string lstrrev = lstr;
        std::reverse(lstrrev.begin(), lstrrev.end());

        std::vector<std::string> a(5, "");

        if (lstrrev.length() % 3 == 1) {
            lstrrev += "00";
        } else if (lstrrev.length() % 3 == 2) {
            lstrrev += "0";
        }

        std::string lm;
        for (size_t i = 0; i < lstrrev.length() / 3; i++) {
            std::string sub = lstrrev.substr(3 * i, 3);
            std::reverse(sub.begin(), sub.end());
            a[i] = sub;
            if (a[i] != "000") {
                lm = transThree(a[i]) + " " + parseMore(static_cast<int>(i)) + " " + lm;
            } else {
                lm = transThree(a[i]) + lm;
            }
        }

        std::string xs = !rstr.empty() ? "AND CENTS " + transTwo(rstr) + " " : "";
        if (trim(lm).empty()) {
            return "ZERO ONLY";
        } else {
            return trim(lm) + " " + xs + "ONLY";
        }
    }

    std::string transTwo(const std::string& s) {
        std::string padded = s;
        if (padded.length() < 2) {
            padded = std::string(2 - padded.length(), '0') + padded;
        }

        if (padded[0] == '0') {
            return NUMBER[std::stoi(padded.substr(1))];
        } else if (padded[0] == '1') {
            return NUMBER_TEEN[std::stoi(padded) - 10];
        } else if (padded[1] == '0') {
            return NUMBER_TEN[std::stoi(padded.substr(0, 1)) - 1];
        } else {
            return NUMBER_TEN[std::stoi(padded.substr(0, 1)) - 1] + " " + NUMBER[std::stoi(padded.substr(1))];
        }
    }

    std::string transThree(const std::string& s) {
        if (s[0] == '0') {
            return transTwo(s.substr(1));
        } else if (s.substr(1) == "00") {
            return NUMBER[std::stoi(s.substr(0, 1))] + " HUNDRED";
        } else {
            return NUMBER[std::stoi(s.substr(0, 1))] + " HUNDRED AND " + transTwo(s.substr(1));
        }
    }

    std::string parseMore(int i) {
        return NUMBER_MORE[i];
    }
};