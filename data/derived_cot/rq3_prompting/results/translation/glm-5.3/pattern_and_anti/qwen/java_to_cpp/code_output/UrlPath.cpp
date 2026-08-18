#include <cctype>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace org {
namespace example {

class UrlPath {
private:
    std::vector<std::string> segments;
    bool withEndTag;

    static bool isHexDigit(char c) {
        unsigned char u = static_cast<unsigned char>(c);
        return std::isdigit(u) != 0 ||
               (c >= 'a' && c <= 'f') ||
               (c >= 'A' && c <= 'F');
    }

    static int hexValue(char c) {
        if (c >= '0' && c <= '9') return c - '0';
        if (c >= 'a' && c <= 'f') return c - 'a' + 10;
        return c - 'A' + 10;
    }

    static std::string strip(const std::string& s) {
        std::size_t b = 0, e = s.size();
        while (b < e && std::isspace(static_cast<unsigned char>(s[b])) != 0) ++b;
        while (e > b && std::isspace(static_cast<unsigned char>(s[e - 1])) != 0) --e;
        return s.substr(b, e - b);
    }

    static std::string urlDecode(const std::string& s, const std::string& charset) {
        (void)charset; // decoded bytes returned as-is (exact for UTF-8/ASCII charsets)
        std::string out;
        out.reserve(s.size());
        for (std::size_t i = 0; i < s.size(); ++i) {
            char c = s[i];
            if (c == '+') {
                out += ' ';
            } else if (c == '%') {
                if (i + 2 < s.size() && isHexDigit(s[i + 1]) && isHexDigit(s[i + 2])) {
                    out += static_cast<char>(hexValue(s[i + 1]) * 16 + hexValue(s[i + 2]));
                    i += 2;
                } else {
                    throw std::invalid_argument(
                        "URLDecoder: Incomplete trailing escape (%) pattern");
                }
            } else {
                out += c;
            }
        }
        return out;
    }

public:
    UrlPath() : withEndTag(false) {}

    void add(const std::string& segment) {
        segments.push_back(fixPath(segment));
    }

    void parse(const std::string& path, const std::string& charset) {
        if (!path.empty()) {
            if (path.back() == '/') {
                withEndTag = true;
            }

            std::string fixed = fixPath(path);
            if (!fixed.empty()) {
                // Java String.split("/"): keeps interior empties, drops trailing empties
                std::vector<std::string> split;
                std::size_t start = 0;
                for (std::size_t i = 0; i <= fixed.size(); ++i) {
                    if (i == fixed.size() || fixed[i] == '/') {
                        split.push_back(fixed.substr(start, i - start));
                        start = i + 1;
                    }
                }
                while (!split.empty() && split.back().empty()) {
                    split.pop_back();
                }

                for (const std::string& seg : split) {
                    try {
                        segments.push_back(urlDecode(seg, charset));
                    } catch (const std::exception& e) {
                        std::cerr << e.what() << std::endl; // e.printStackTrace() -> stderr
                    }
                }
            }
        }
    }

    static std::string fixPath(const std::string& path) {
        if (path.empty()) {
            return "";
        }

        std::string segmentStr = strip(path);
        // replaceAll("^/+|/+$", ""): strip leading/trailing slashes
        std::size_t b = segmentStr.find_first_not_of('/');
        if (b == std::string::npos) {
            return "";
        }
        std::size_t e = segmentStr.find_last_not_of('/');
        return segmentStr.substr(b, e - b + 1);
    }

    const std::vector<std::string>& getSegments() const {
        return segments;
    }

    bool isWithEndTag() const {
        return withEndTag;
    }
};

} // namespace example
} // namespace org