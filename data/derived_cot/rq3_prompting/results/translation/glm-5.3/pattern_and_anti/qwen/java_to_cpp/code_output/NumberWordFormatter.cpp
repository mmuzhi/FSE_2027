#include <array>
#include <cstddef>
#include <optional>
#include <stdexcept>
#include <string>
#include <vector>

namespace org::example {

class NumberWordFormatter {
private:
    const std::array<std::string, 10> NUMBER = {"", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"};
    const std::array<std::string, 10> NUMBER_TEEN = {"TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN"};
    const std::array<std::string, 9> NUMBER_TEN = {"TEN", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"};
    const std::array<std::string, 4> NUMBER_MORE = {"", "THOUSAND", "MILLION", "BILLION"};
    const std::array<std::string, 16> NUMBER_SUFFIX = {"k", "w", "", "m", "", "", "b", "", "", "t", "", "", "p", "", "", "e"};

    // Mirrors Integer.parseInt: throws std::invalid_argument (NumberFormatException analog)
    // on malformed input or int overflow.
    static int parseInt(const std::string& s) {
        std::size_t i = 0;
        bool neg = false;
        if (i < s.size() && (s[i] == '+' || s[i] == '-')) {
            neg = (s[i] == '-');
            ++i;
        }
        if (i == s.size()) throw std::invalid_argument("For input string: \"" + s + "\"");
        long long v = 0;
        for (; i < s.size(); ++i) {
            const char c = s[i];
            if (c < '0' || c > '9') throw std::invalid_argument("For input string: \"" + s + "\"");
            v = v * 10 + (c - '0');
            if (v > 2147483648LL) throw std::invalid_argument("For input string: \"" + s + "\"");
        }
        const long long r = neg ? -v : v;
        if (r < -2147483648LL || r > 2147483647LL) {
            throw std::invalid_argument("For input string: \"" + s + "\"");
        }
        return static_cast<int>(r);
    }

    // Mirrors String.trim(): removes leading/trailing chars <= U+0020.
    static std::string trim(const std::string& s) {
        std::size_t b = 0, e = s.size();
        while (b < e && static_cast<unsigned char>(s[b]) <= ' ') ++b;
        while (e > b && static_cast<unsigned char>(s[e - 1]) <= ' ') --e;
        return s.substr(b, e - b);
    }

public:
    // Java: format(Object x) with null -> ""; modeled with std::optional.
    std::string format(const std::optional<std::string>& x) const {
        if (!x.has_value()) {
            return "";
        }
        return formatString(*x);
    }

    std::string formatString(const std::string& x) const {
        // Java String.split("\\."): drops trailing empty segments.
        std::vector<std::string> parts;
        std::string cur;
        for (char c : x) {
            if (c == '.') { parts.push_back(cur); cur.clear(); }
            else { cur += c; }
        }
        parts.push_back(cur);
        while (!parts.empty() && parts.back().empty()) parts.pop_back();

        const std::string& lstr = parts.at(0); // throws (like AIOOBE) if x is only dots
        std::string rstr = parts.size() > 1 ? parts[1] : "";
        std::string lstrrev(lstr.rbegin(), lstr.rend());
        std::vector<std::string> a(5);

        if (lstrrev.size() % 3 == 1) {
            lstrrev += "00";
        } else if (lstrrev.size() % 3 == 2) {
            lstrrev += "0";
        }

        std::string lm;
        for (std::size_t i = 0; i < lstrrev.size() / 3; i++) {
            const std::string chunk = lstrrev.substr(3 * i, 3);
            a.at(i) = std::string(chunk.rbegin(), chunk.rend()); // throws at i >= 5 (like AIOOBE)
            if (a[i] != "000") {
                lm.insert(0, transThree(a[i]) + " " + parseMore(static_cast<int>(i)) + " ");
            } else {
                lm.insert(0, transThree(a[i]));
            }
        }

        const std::string xs = !rstr.empty() ? "AND CENTS " + transTwo(rstr) + " " : "";
        if (trim(lm).empty()) {
            return "ZERO ONLY";
        } else {
            return trim(lm) + " " + xs + "ONLY";
        }
    }

    std::string transTwo(std::string s) const {
        // String.format("%2s", s).replace(' ', '0')
        if (s.size() < 2) s.insert(0, 2 - s.size(), ' ');
        for (char& c : s) if (c == ' ') c = '0';
        if (s[0] == '0') {
            return NUMBER.at(parseInt(s.substr(1)));
        } else if (s[0] == '1') {
            return NUMBER_TEEN.at(parseInt(s) - 10);
        } else if (s[1] == '0') {
            return NUMBER_TEN.at(parseInt(s.substr(0, 1)) - 1);
        } else {
            return NUMBER_TEN.at(parseInt(s.substr(0, 1)) - 1) + " " + NUMBER.at(parseInt(s.substr(1)));
        }
    }

    std::string transThree(const std::string& s) const {
        if (s.empty()) throw std::out_of_range("char index 0 out of range");
        if (s[0] == '0') {
            return transTwo(s.substr(1));
        } else if (s.substr(1) == "00") {
            return NUMBER.at(parseInt(s.substr(0, 1))) + " HUNDRED";
        } else {
            return NUMBER.at(parseInt(s.substr(0, 1))) + " HUNDRED AND " + transTwo(s.substr(1));
        }
    }

    std::string parseMore(int i) const {
        return NUMBER_MORE.at(static_cast<std::size_t>(i)); // throws at i >= 4 (like AIOOBE)
    }
};

} // namespace org::example