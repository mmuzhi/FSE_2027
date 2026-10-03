#include <string>
#include <vector>
#include <sstream>
#include <algorithm>
#include <iostream>

class NumberWordFormatter {
private:
    const std::vector<std::string> NUMBER = {"", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"};
    const std::vector<std::string> NUMBER_TEEN = {"TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN"};
    const std::vector<std::string> NUMBER_TEN = {"TEN", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"};
    const std::vector<std::string> NUMBER_MORE = {"", "THOUSAND", "MILLION", "BILLION"};
    const std::vector<std::string> NUMBER_SUFFIX = {"k", "w", "", "m", "", "", "b", "", "", "t", "", "", "p", "", "", "e"};

    std::string transTwo(const std::string& s) {
        std::string padded = s;
        while (padded.length() < 2) {
            padded = "0" + padded;
        }
        if (padded[0] == '0') {
            return NUMBER[std::stoi(padded.substr(1))];
        } else if (padded[0] == '1') {
            int idx = std::stoi(padded) - 10;
            return NUMBER_TEEN[idx];
        } else if (padded[1] == '0') {
            int idx = std::stoi(padded.substr(0,1)) - 1;
            return NUMBER_TEN[idx];
        } else {
            int idx_tens = std::stoi(padded.substr(0,1)) - 1;
            int idx_units = std::stoi(padded.substr(1));
            return NUMBER_TEN[idx_tens] + " " + NUMBER[idx_units];
        }
    }

    std::string transThree(const std::string& s) {
        if (s[0] == '0') {
            return transTwo(s.substr(1));
        } else if (s.substr(1) == "00") {
            return NUMBER[std::stoi(s.substr(0,1))] + " HUNDRED";
        } else {
            return NUMBER[std::stoi(s.substr(0,1))] + " HUNDRED AND " + transTwo(s.substr(1));
        }
    }

    std::string parseMore(int i) {
        return NUMBER_MORE[i];
    }

public:
    std::string format(const char* x) {
        if (x == nullptr) {
            return "";
        }
        return formatString(std::string(x));
    }

    std::string format(const std::string& x) {
        return formatString(x);
    }

    std::string formatString(const std::string& x) {
        size_t dotPos = x.find('.');
        std::string lstr = (dotPos == std::string::npos) ? x : x.substr(0, dotPos);
        std::string rstr = (dotPos == std::string::npos) ? "" : x.substr(dotPos + 1);

        std::string lstrrev = lstr;
        std::reverse(lstrrev.begin(), lstrrev.end());

        if (lstrrev.length() % 3 == 1) {
            lstrrev += "00";
        } else if (lstrrev.length() % 3 == 2) {
            lstrrev += "0";
        }

        std::string lm;
        int chunkCount = static_cast<int>(lstrrev.length() / 3);
        for (int i = 0; i < chunkCount; ++i) {
            std::string chunk = lstrrev.substr(3 * i, 3);
            std::reverse(chunk.begin(), chunk.end());
            if (chunk != "000") {
                std::string part = transThree(chunk) + " " + parseMore(i) + " ";
                lm.insert(0, part);
            } else {
                std::string part = transThree(chunk);
                lm.insert(0, part);
            }
        }

        std::string xs;
        if (!rstr.empty()) {
            xs = "AND CENTS " + transTwo(rstr) + " ";
        }

        std::string trimmed = lm;
        size_t first = trimmed.find_first_not_of(' ');
        size_t last = trimmed.find_last_not_of(' ');
        if (first == std::string::npos) {
            trimmed = "";
        } else {
            trimmed = trimmed.substr(first, last - first + 1);
        }

        if (trimmed.empty()) {
            return "ZERO ONLY";
        } else {
            return trimmed + " " + xs + "ONLY";
        }
    }
};