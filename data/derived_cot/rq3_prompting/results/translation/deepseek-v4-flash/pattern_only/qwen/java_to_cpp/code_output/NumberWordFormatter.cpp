#include <string>
#include <vector>
#include <array>
#include <stdexcept>

class NumberWordFormatter {
private:
    const std::array<std::string, 10> NUMBER = {"", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"};
    const std::array<std::string, 10> NUMBER_TEEN = {"TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN"};
    const std::array<std::string, 9> NUMBER_TEN = {"TEN", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"};
    const std::array<std::string, 4> NUMBER_MORE = {"", "THOUSAND", "MILLION", "BILLION"};

    static std::vector<std::string> split(const std::string& s, char delim) {
        std::vector<std::string> parts;
        std::string cur;
        for (char c : s) {
            if (c == delim) {
                parts.push_back(cur);
                cur.clear();
            } else {
                cur += c;
            }
        }
        parts.push_back(cur);
        while (parts.size() > 1 && parts.back().empty()) {
            parts.pop_back();
        }
        return parts;
    }

    static std::string trim(const std::string& s) {
        size_t start = 0;
        while (start < s.size() && s[start] <= ' ') {
            ++start;
        }
        size_t end = s.size();
        while (end > start && s[end - 1] <= ' ') {
            --end;
        }
        return s.substr(start, end - start);
    }

    std::string transTwo(std::string s) const {
        if (s.length() < 2) {
            s.insert(0, 2 - s.length(), ' ');
        }
        for (char& c : s) {
            if (c == ' ') {
                c = '0';
            }
        }

        if (s[0] == '0') {
            return NUMBER.at(std::stoi(s.substr(1)));
        } else if (s[0] == '1') {
            return NUMBER_TEEN.at(std::stoi(s) - 10);
        } else if (s[1] == '0') {
            return NUMBER_TEN.at(std::stoi(s.substr(0, 1)) - 1);
        } else {
            return NUMBER_TEN.at(std::stoi(s.substr(0, 1)) - 1) + " " + NUMBER.at(std::stoi(s.substr(1)));
        }
    }

    std::string transThree(const std::string& s) const {
        if (s[0] == '0') {
            return transTwo(s.substr(1));
        } else if (s.substr(1) == "00") {
            return NUMBER.at(std::stoi(s.substr(0, 1))) + " HUNDRED";
        } else {
            return NUMBER.at(std::stoi(s.substr(0, 1))) + " HUNDRED AND " + transTwo(s.substr(1));
        }
    }

    std::string parseMore(int i) const {
        return NUMBER_MORE.at(i);
    }

public:
    std::string format(const std::string& x) const {
        return formatString(x);
    }

    std::string format(const char* x) const {
        if (x == nullptr) {
            return "";
        }
        return formatString(std::string(x));
    }

    std::string formatString(const std::string& x) const {
        std::vector<std::string> parts = split(x, '.');
        std::string lstr = parts[0];
        std::string rstr = parts.size() > 1 ? parts[1] : "";
        std::string lstrrev(lstr.rbegin(), lstr.rend());

        if (lstrrev.length() % 3 == 1) {
            lstrrev += "00";
        } else if (lstrrev.length() % 3 == 2) {
            lstrrev += "0";
        }

        std::array<std::string, 5> a;
        std::string lm;

        for (int i = 0; i < static_cast<int>(lstrrev.length() / 3); ++i) {
            std::string chunk = lstrrev.substr(3 * i, 3);
            std::string rev(chunk.rbegin(), chunk.rend());
            a.at(i) = rev;

            if (a.at(i) != "000") {
                std::string t3 = transThree(a.at(i));
                std::string more = parseMore(i);
                lm.insert(0, t3 + " " + more + " ");
            } else {
                lm.insert(0, transThree(a.at(i)));
            }
        }

        std::string xs;
        if (!rstr.empty()) {
            xs = "AND CENTS " + transTwo(rstr) + " ";
        }

        std::string trimmed = trim(lm);
        if (trimmed.empty()) {
            return "ZERO ONLY";
        } else {
            return trimmed + " " + xs + "ONLY";
        }
    }
};