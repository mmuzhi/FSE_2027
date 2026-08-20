#include <algorithm>
#include <array>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace org {
namespace example {

class NumberWordFormatter {
private:
    const std::array<std::string, 10> NUMBER = {"", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"};
    const std::array<std::string, 10> NUMBER_TEEN = {"TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN"};
    const std::array<std::string, 9> NUMBER_TEN = {"TEN", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"};
    const std::array<std::string, 4> NUMBER_MORE = {"", "THOUSAND", "MILLION", "BILLION"};
    const std::array<std::string, 16> NUMBER_SUFFIX = {"k", "w", "", "m", "", "", "b", "", "", "t", "", "", "p", "", "", "e"};

    // Equivalent of Java's String.trim(): removes leading/trailing chars <= ' '
    static std::string trim(const std::string& s) {
        std::size_t b = 0, e = s.size();
        while (b < e && static_cast<unsigned char>(s[b]) <= ' ') ++b;
        while (e > b && static_cast<unsigned char>(s[e - 1]) <= ' ') --e;
        return s.substr(b, e - b);
    }

    // Analogous to Integer.parseInt (throws on invalid input)
    static int toInt(const std::string& s) {
        return std::stoi(s);
    }

public:
    // Analogous to format(Object x); nullptr mirrors the null check
    std::string format(const char* x) {
        if (x == nullptr) {
            return "";
        }
        return formatString(std::string(x));
    }

    std::string format(const std::string& x) {
        return formatString(x);
    }

    template <typename T>
    std::string format(const T& x) {
        std::ostringstream oss;
        oss << x;
        return formatString(oss.str());
    }

    std::string formatString(const std::string& x) {
        // Mimics Java's x.split("\\.") with default limit
        // (trailing empty strings removed; no-dot input yields the input itself)
        std::vector<std::string> parts;
        std::size_t start = 0;
        bool found = false;
        for (std::size_t i = 0; i < x.size(); ++i) {
            if (x[i] == '.') {
                found = true;
                parts.push_back(x.substr(start, i - start));
                start = i + 1;
            }
        }
        if (!found) {
            parts.push_back(x);
        } else {
            parts.push_back(x.substr(start));
            while (!parts.empty() && parts.back().empty()) {
                parts.pop_back();
            }
        }

        std::string lstr = parts.at(0); // throws if x was only dots, mirroring Java
        std::string rstr = parts.size() > 1 ? parts[1] : "";
        std::string lstrrev(lstr.rbegin(), lstr.rend());
        std::array<std::string, 5> a;

        if (lstrrev.size() % 3 == 1) {
            lstrrev += "00";
        } else if (lstrrev.size() % 3 == 2) {
            lstrrev += "0";
        }

        std::string lm;
        for (std::size_t i = 0; i < lstrrev.size() / 3; i++) {
            std::string grp = lstrrev.substr(3 * i, 3);
            a.at(i) = std::string(grp.rbegin(), grp.rend()); // at() mirrors Java bounds check
            if (a[i] != "000") {
                lm.insert(0, transThree(a[i]) + " " + parseMore(static_cast<int>(i)) + " ");
            } else {
                lm.insert(0, transThree(a[i]));
            }
        }

        std::string xs = !rstr.empty() ? "AND CENTS " + transTwo(rstr) + " " : "";
        if (trim(lm).empty()) {
            return "ZERO ONLY";
        } else {
            return trim(lm) + " " + xs + "ONLY";
        }
    }

    std::string transTwo(std::string s) {
        // Mimics String.format("%2s", s).replace(' ', '0')
        if (s.size() < 2) {
            s.insert(0, 2 - s.size(), ' ');
        }
        std::replace(s.begin(), s.end(), ' ', '0');
        if (s[0] == '0') {
            return NUMBER.at(toInt(s.substr(1)));
        } else if (s[0] == '1') {
            return NUMBER_TEEN.at(toInt(s) - 10);
        } else if (s[1] == '0') {
            return NUMBER_TEN.at(toInt(s.substr(0, 1)) - 1);
        } else {
            return NUMBER_TEN.at(toInt(s.substr(0, 1)) - 1) + " " + NUMBER.at(toInt(s.substr(1)));
        }
    }

    std::string transThree(const std::string& s) {
        if (s.empty()) {
            throw std::out_of_range("transThree: empty string"); // mirrors charAt(0) on ""
        }
        if (s[0] == '0') {
            return transTwo(s.substr(1));
        } else if (s.substr(1) == "00") {
            return NUMBER.at(toInt(s.substr(0, 1))) + " HUNDRED";
        } else {
            return NUMBER.at(toInt(s.substr(0, 1))) + " HUNDRED AND " + transTwo(s.substr(1));
        }
    }

    std::string parseMore(int i) {
        return NUMBER_MORE.at(i); // at() mirrors Java's ArrayIndexOutOfBoundsException
    }
};

} // namespace example
} // namespace org