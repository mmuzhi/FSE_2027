#include <string>
#include <vector>
#include <optional>
#include <algorithm>
#include <charconv>
#include <stdexcept>

class NumberWordFormatter {
public:
    std::vector<std::string> NUMBER;
    std::vector<std::string> NUMBER_TEEN;
    std::vector<std::string> NUMBER_TEN;
    std::vector<std::string> NUMBER_MORE;
    std::vector<std::string> NUMBER_SUFFIX;

    NumberWordFormatter()
        : NUMBER({"", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"}),
          NUMBER_TEEN({"TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN",
                       "SEVENTEEN", "EIGHTEEN", "NINETEEN"}),
          NUMBER_TEN({"TEN", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"}),
          NUMBER_MORE({"", "THOUSAND", "MILLION", "BILLION"}),
          NUMBER_SUFFIX({"k", "w", "", "m", "", "", "b", "", "", "t", "", "", "p", "", "", "e"}) {}

    // Mirrors Python's format(x): None -> "", otherwise str(x) -> format_string
    std::string format(std::optional<double> x) {
        if (x.has_value()) {
            return format_string(py_str(*x));
        }
        return "";
    }

    std::string format(const std::string& x) {
        return format_string(x);
    }

    std::string format(const char* x) {
        return format_string(std::string(x));
    }

    std::string format_string(std::string x) {
        // Equivalent of: lstr, rstr = (x.split('.') + [''])[:2]
        std::string lstr = x;
        std::string rstr = "";
        std::string::size_type pos = x.find('.');
        if (pos != std::string::npos) {
            lstr = x.substr(0, pos);
            std::string rest = x.substr(pos + 1);
            std::string::size_type pos2 = rest.find('.');
            rstr = (pos2 == std::string::npos) ? rest : rest.substr(0, pos2);
        }

        std::string lstrrev(lstr.rbegin(), lstr.rend());
        if (lstrrev.size() % 3 == 1) {
            lstrrev += "00";
        } else if (lstrrev.size() % 3 == 2) {
            lstrrev += "0";
        }

        std::string lm = "";
        for (std::size_t i = 0; i < lstrrev.size() / 3; ++i) {
            std::string chunk = lstrrev.substr(3 * i, 3);
            std::reverse(chunk.begin(), chunk.end());
            if (chunk != "000") {
                lm = trans_three(chunk) + " " + parse_more(i) + " " + lm;
            } else {
                lm += trans_three(chunk);
            }
        }

        std::string xs = rstr.empty() ? std::string("")
                                      : ("AND CENTS " + trans_two(rstr) + " ");
        std::string trimmed = strip(lm);
        if (trimmed.empty()) {
            return "ZERO ONLY";
        }
        return trimmed + " " + xs + "ONLY";
    }

    std::string trans_two(std::string s) {
        // zfill(2)
        if (s.size() < 2) {
            s.insert(0, 2 - s.size(), '0');
        }
        if (s[0] == '0') {
            return NUMBER.at(s.back() - '0');
        } else if (s[0] == '1') {
            return NUMBER_TEEN.at(std::stol(s) - 10);
        } else if (s[1] == '0') {
            return NUMBER_TEN.at(s[0] - '1');
        } else {
            return NUMBER_TEN.at(s[0] - '1') + " " + NUMBER.at(s.back() - '0');
        }
    }

    std::string trans_three(const std::string& s) {
        if (s[0] == '0') {
            return trans_two(s.substr(1));
        } else if (s.substr(1) == "00") {
            return NUMBER.at(s[0] - '0') + " HUNDRED";
        } else {
            return NUMBER.at(s[0] - '0') + " HUNDRED AND " + trans_two(s.substr(1));
        }
    }

    std::string parse_more(std::size_t i) {
        return NUMBER_MORE.at(i);
    }

private:
    static std::string strip(const std::string& s) {
        const char* ws = " \t\n\r\f\v";
        std::string::size_type b = s.find_first_not_of(ws);
        if (b == std::string::npos) return "";
        std::string::size_type e = s.find_last_not_of(ws);
        return s.substr(b, e - b + 1);
    }

    // Shortest round-trip representation, mirroring Python's str() for numbers
    static std::string py_str(double v) {
        char buf[64];
        auto res = std::to_chars(buf, buf + sizeof(buf), v);
        return std::string(buf, res.ptr);
    }
};