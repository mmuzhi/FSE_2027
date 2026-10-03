#include <string>
#include <vector>
#include <sstream>
#include <algorithm>
#include <cctype>
#include <regex>
#include <stdexcept>
#include <iostream>

class UrlPath {
private:
    std::vector<std::string> segments;
    bool withEndTag;

    static std::string fixPath(const std::string& path) {
        if (path.empty()) return "";
        std::string s = path;
        // strip leading/trailing whitespace (strip)
        size_t start = s.find_first_not_of(" \t\n\r\f\v");
        size_t end = s.find_last_not_of(" \t\n\r\f\v");
        if (start == std::string::npos) return "";
        s = s.substr(start, end - start + 1);
        // remove leading and trailing slashes
        std::regex re("^/+|/+$");
        s = std::regex_replace(s, re, "");
        return s;
    }

    static std::string urlDecode(const std::string& encoded, const std::string& charset) {
        // Simple URL decode using charset (assuming UTF-8 or other)
        // This is a simplified implementation that works for ASCII and percent-encoded bytes.
        // For full charset support, consider using a library such as cpprestsdk or Boost.Beast.
        // Since Java's URLDecoder.decode handles any charset, we'll implement a basic version.
        std::string result;
        size_t i = 0;
        while (i < encoded.size()) {
            if (encoded[i] == '%') {
                if (i + 2 < encoded.size()) {
                    int value;
                    std::istringstream hex(encoded.substr(i + 1, 2));
                    hex >> std::hex >> value;
                    result += static_cast<char>(value);
                    i += 3;
                } else {
                    result += encoded[i];
                    ++i;
                }
            } else if (encoded[i] == '+') {
                result += ' ';
                ++i;
            } else {
                result += encoded[i];
                ++i;
            }
        }
        return result;
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
                std::stringstream ss(fixed);
                std::string seg;
                while (std::getline(ss, seg, '/')) {
                    try {
                        std::string decoded = urlDecode(seg, charset);
                        segments.push_back(decoded);
                    } catch (const std::exception& e) {
                        std::cerr << e.what() << std::endl;
                    }
                }
            }
        }
    }

    std::vector<std::string> getSegments() const {
        return segments;
    }

    bool isWithEndTag() const {
        return withEndTag;
    }
};