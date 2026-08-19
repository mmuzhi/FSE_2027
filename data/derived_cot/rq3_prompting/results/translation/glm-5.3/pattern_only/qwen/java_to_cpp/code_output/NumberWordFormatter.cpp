#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

class NumberWordFormatter {
private:
    const std::vector<std::string> NUMBER = {"", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"};
    const std::vector<std::string> NUMBER_TEEN = {"TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN"};
    const std::vector<std::string> NUMBER_TEN = {"TEN", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"};
    const std::vector<std::string> NUMBER_MORE = {"", "THOUSAND", "MILLION", "BILLION"};
    const std::vector<std::string> NUMBER_SUFFIX = {"k", "w", "", "m", "", "", "b", "", "", "t", "", "", "p", "", "", "e"};

    // Java-like array access: throws std::out_of_range like ArrayIndexOutOfBoundsException.
    static const std::string& at(const std::vector<std::string>& v, int index) {
        if (index < 0 || static_cast<std::size_t>(index) >= v.size()) {
            throw std::out_of_range("Index " + std::to_string(index) +
                                    " out of bounds for length " + std::to_string(v.size()));
        }
        return v[static_cast<std::size_t>(index)];
    }

    static std::string reverseString(const std::string& s) {
        return std::string(s.rbegin(), s.rend());
    }

    // Mimics Java String.trim(): strips leading/trailing chars <= U+0020.
    static std::string trim(const std::string& s) {
        std::size_t b = 0, e = s.size();
        while (b < e && static_cast<unsigned char>(s[b]) <= 0x20) ++b;
        while (e > b && static_cast<unsigned char>(s[e - 1]) <= 0x20) --e;
        return s.substr(b, e - b);
    }

    // Mimics Java String.split("\\.") with limit 0: trailing empty strings removed.
    static std::vector<std::string> splitOnDot(const std::string& x) {
        std::vector<std::string> parts;
        std::string cur;
        for (char c : x) {
            if (c == '.') { parts.push_back(cur); cur.clear(); }
            else { cur += c; }
        }
        parts.push_back(cur);
        while (!parts.empty() && parts.back().empty()) parts.pop_back();
        return parts;
    }

    // Mimics Integer.parseInt; throws std::invalid_argument like NumberFormatException on bad input.
    static int parseInt(const std::string& s) {
        std::size_t pos = 0;
        int value;
        try {
            value = std::stoi(s, &pos);
        } catch (...) {
            throw std::invalid_argument("For input string: \"" + s + "\"");
        }
        if (pos != s.size()) {
            throw std::invalid_argument("For input string: \"" + s + "\"");
        }
        return value;
    }

public:
    // Java: format(null) -> ""
    std::string format(std::nullptr_t) { return ""; }

    std::string format(const std::string& x) { return formatString(x); }

    std::string format(const char* x) {
        return x == nullptr ? std::string() : formatString(std::string(x));
    }

    // Generic stand-in for format(Object): converts via stream like Object.toString().
    template <typename T>
    std::string format(const T& x) {
        std::ostringstream oss;
        oss << x;
        return formatString(oss.str());
    }

    std::string formatString(const std::string& x) {
        std::vector<std::string> parts = splitOnDot(x);
        std::string lstr = parts.at(0);  // throws std::out_of_range like Java parts[0] when split is empty (e.g. input ".")
        std::string rstr = parts.size() > 1 ? parts[1] : std::string();
        std::string lstrrev = reverseString(lstr);
        std::vector<std::string> a(5);

        if (lstrrev.size() % 3 == 1) {
            lstrrev += "00";
        } else if (lstrrev.size() % 3 == 2) {
            lstrrev += "0";
        }

        std::string lm;
        for (std::size_t i = 0; i < lstrrev.size() / 3; i++) {
            a.at(i) = reverseString(lstrrev.substr(3 * i, 3));  // throws like AIOOBE when i >= 5
            if (a[i] != "000") {
                lm = transThree(a[i]) + " " + parseMore(static_cast<int>(i)) + " " + lm;
            } else {
                lm = transThree(a[i]) + lm;
            }
        }

        std::string xs = !rstr.empty() ? "AND CENTS " + transTwo(rstr) + " " : std::string();
        std::string lmTrimmed = trim(lm);
        if (lmTrimmed.empty()) {
            return "ZERO ONLY";
        }
        return lmTrimmed + " " + xs + "ONLY";
    }

    std::string transTwo(const std::string& str) const {
        // Mimics String.format("%2s", s).replace(' ', '0')
        std::string s = str.size() >= 2 ? str : std::string(2 - str.size(), ' ') + str;
        for (char& c : s) {
            if (c == ' ') c = '0';
        }
        if (s[0] == '0') {
            return at(NUMBER, parseInt(s.substr(1)));
        } else if (s[0] == '1') {
            return at(NUMBER_TEEN, parseInt(s) - 10);
        } else if (s[1] == '0') {
            return at(NUMBER_TEN, parseInt(s.substr(0, 1)) - 1);
        } else {
            return at(NUMBER_TEN, parseInt(s.substr(0, 1)) - 1) + " " + at(NUMBER, parseInt(s.substr(1)));
        }
    }

    std::string transThree(const std::string& s) const {
        if (s[0] == '0') {
            return transTwo(s.substr(1));
        } else if (s.substr(1) == "00") {
            return at(NUMBER, parseInt(s.substr(0, 1))) + " HUNDRED";
        } else {
            return at(NUMBER, parseInt(s.substr(0, 1))) + " HUNDRED AND " + transTwo(s.substr(1));
        }
    }

    std::string parseMore(int i) const {
        return at(NUMBER_MORE, i);
    }
};