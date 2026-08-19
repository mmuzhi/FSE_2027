#pragma once

#include <cctype>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

class UrlPath {
private:
    std::vector<std::string> segments;
    bool withEndTag = false;

    static int hexValue(char c) {
        if (c >= '0' && c <= '9') return c - '0';
        if (c >= 'a' && c <= 'f') return c - 'a' + 10;
        if (c >= 'A' && c <= 'F') return c - 'A' + 10;
        return -1;
    }

    // Equivalent of java.net.URLDecoder.decode(s, charset):
    // '+' -> ' ', %XX -> byte; throws on incomplete/illegal escape.
    // Decoded bytes map directly to the string for UTF-8 / single-byte charsets.
    static std::string urlDecode(const std::string& s, const std::string& charset) {
        (void)charset; // byte-transparent for UTF-8 / single-byte charsets
        std::string out;
        out.reserve(s.size());
        for (std::size_t i = 0; i < s.size(); ++i) {
            char c = s[i];
            if (c == '+') {
                out += ' ';
            } else if (c == '%') {
                if (i + 2 >= s.size()) {
                    throw std::invalid_argument(
                        "URLDecoder: Incomplete trailing escape (%) pattern");
                }
                int hi = hexValue(s[i + 1]);
                int lo = hexValue(s[i + 2]);
                if (hi < 0 || lo < 0) {
                    throw std::invalid_argument(
                        "URLDecoder: Illegal hex characters in escape (%) pattern");
                }
                out += static_cast<char>((hi << 4) | lo);
                i += 2;
            } else {
                out += c;
            }
        }
        return out;
    }

public:
    UrlPath() = default;

    void add(const std::string& segment) {
        segments.push_back(fixPath(segment));
    }

    void parse(const std::string& path, const std::string& charset) {
        if (!path.empty()) {  // Java: path != null && !path.isEmpty()
            if (path.back() == '/') {
                withEndTag = true;
            }

            std::string fixed = fixPath(path);
            if (!fixed.empty()) {
                // Split on '/', preserving interior empty segments
                // (Java split drops only trailing empties, impossible after fixPath).
                std::vector<std::string> split;
                std::size_t start = 0;
                while (true) {
                    std::size_t pos = fixed.find('/', start);
                    if (pos == std::string::npos) {
                        split.push_back(fixed.substr(start));
                        break;
                    }
                    split.push_back(fixed.substr(start, pos - start));
                    start = pos + 1;
                }

                for (const std::string& seg : split) {
                    try {
                        segments.push_back(urlDecode(seg, charset));
                    } catch (const std::exception& e) {
                        // Java: e.printStackTrace() -> report to stderr, skip segment
                        std::cerr << e.what() << std::endl;
                    }
                }
            }
        }
    }

    static std::string fixPath(const std::string& path) {
        if (path.empty()) {  // covers null/empty -> ""
            return "";
        }

        // strip() : trim whitespace at both ends
        std::size_t b = 0, e = path.size();
        while (b < e && std::isspace(static_cast<unsigned char>(path[b]))) ++b;
        while (e > b && std::isspace(static_cast<unsigned char>(path[e - 1]))) --e;
        std::string trimmed = path.substr(b, e - b);

        // replaceAll("^/+|/+$", "") : remove all leading and trailing slashes
        std::size_t lb = 0;
        while (lb < trimmed.size() && trimmed[lb] == '/') ++lb;
        std::size_t re = trimmed.size();
        while (re > lb && trimmed[re - 1] == '/') --re;

        return trimmed.substr(lb, re - lb);
    }

    const std::vector<std::string>& getSegments() const {
        return segments;
    }

    bool isWithEndTag() const {
        return withEndTag;
    }
};