#include <string>
#include <vector>
#include <cctype>
#include <iostream>
#include <stdexcept>

class UrlPath {
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
                std::vector<std::string> parts = split(fixed, '/');
                for (const std::string& seg : parts) {
                    try {
                        segments.push_back(urlDecode(seg, charset));
                    } catch (const std::exception& e) {
                        std::cerr << e.what() << std::endl;
                    }
                }
            }
        }
    }

    static std::string fixPath(const std::string& path) {
        if (path.empty()) {
            return "";
        }

        std::string s = strip(path);
        size_t start = s.find_first_not_of('/');
        if (start == std::string::npos) {
            return "";
        }
        size_t end = s.find_last_not_of('/');
        return s.substr(start, end - start + 1);
    }

    std::vector<std::string>& getSegments() {
        return segments;
    }

    bool isWithEndTag() const {
        return withEndTag;
    }

private:
    std::vector<std::string> segments;
    bool withEndTag;

    static std::string strip(const std::string& s) {
        size_t start = 0;
        while (start < s.size() && std::isspace(static_cast<unsigned char>(s[start]))) {
            ++start;
        }
        size_t end = s.size();
        while (end > start && std::isspace(static_cast<unsigned char>(s[end - 1]))) {
            --end;
        }
        return s.substr(start, end - start);
    }

    static std::vector<std::string> split(const std::string& s, char delim) {
        std::vector<std::string> result;
        size_t start = 0;
        while (start <= s.size()) {
            size_t pos = s.find(delim, start);
            if (pos == std::string::npos) {
                result.push_back(s.substr(start));
                break;
            }
            result.push_back(s.substr(start, pos - start));
            start = pos + 1;
        }
        return result;
    }

    static int hexVal(char c) {
        if (c >= '0' && c <= '9') return c - '0';
        if (c >= 'a' && c <= 'f') return c - 'a' + 10;
        if (c >= 'A' && c <= 'F') return c - 'A' + 10;
        return 0;
    }

    static std::string toLower(std::string s) {
        for (char& c : s) {
            c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
        }
        return s;
    }

    static std::string decodeUtf8(const std::string& bytes) {
        std::string out;
        size_t i = 0;
        while (i < bytes.size()) {
            unsigned char c = static_cast<unsigned char>(bytes[i]);
            if (c < 0x80) {
                out += static_cast<char>(c);
                ++i;
            } else {
                int len = 0;
                unsigned int cp = 0;
                if ((c & 0xE0) == 0xC0) {
                    len = 2;
                    cp = c & 0x1F;
                } else if ((c & 0xF0) == 0xE0) {
                    len = 3;
                    cp = c & 0x0F;
                } else if ((c & 0xF8) == 0xF0) {
                    len = 4;
                    cp = c & 0x07;
                } else {
                    out += "\xEF\xBF\xBD";
                    ++i;
                    continue;
                }

                if (i + len > bytes.size()) {
                    out += "\xEF\xBF\xBD";
                    ++i;
                    continue;
                }

                bool valid = true;
                for (int j = 1; j < len; ++j) {
                    unsigned char cc = static_cast<unsigned char>(bytes[i + j]);
                    if ((cc & 0xC0) != 0x80) {
                        valid = false;
                        break;
                    }
                    cp = (cp << 6) | (cc & 0x3F);
                }

                if (len == 2 && cp < 0x80) valid = false;
                if (len == 3 && cp < 0x800) valid = false;
                if (len == 4 && cp < 0x10000) valid = false;
                if (cp >= 0xD800 && cp <= 0xDFFF) valid = false;
                if (cp > 0x10FFFF) valid = false;

                if (!valid) {
                    out += "\xEF\xBF\xBD";
                    ++i;
                } else {
                    out.append(bytes, i, len);
                    i += len;
                }
            }
        }
        return out;
    }

    static std::string latin1ToUtf8(const std::string& bytes) {
        std::string out;
        for (unsigned char b : bytes) {
            if (b < 0x80) {
                out += static_cast<char>(b);
            } else {
                out += static_cast<char>(0xC0 | (b >> 6));
                out += static_cast<char>(0x80 | (b & 0x3F));
            }
        }
        return out;
    }

    static std::string asciiToUtf8(const std::string& bytes) {
        std::string out;
        for (unsigned char b : bytes) {
            if (b < 0x80) {
                out += static_cast<char>(b);
            } else {
                out += "\xEF\xBF\xBD";
            }
        }
        return out;
    }

    static std::string decodeBytes(const std::string& bytes, const std::string& charset) {
        if (charset.empty()) {
            throw std::runtime_error("Unsupported charset: " + charset);
        }

        std::string cs = toLower(charset);
        if (cs == "utf-8" || cs == "utf8") {
            return decodeUtf8(bytes);
        }
        if (cs == "iso-8859-1" || cs == "iso8859-1" || cs == "latin1" || cs == "latin-1") {
            return latin1ToUtf8(bytes);
        }
        if (cs == "us-ascii" || cs == "ascii") {
            return asciiToUtf8(bytes);
        }

        return bytes;
    }

    static std::string urlDecode(const std::string& str, const std::string& charset) {
        std::string result;
        size_t i = 0;

        while (i < str.size()) {
            char c = str[i];
            if (c == '+') {
                result += ' ';
                ++i;
            } else if (c == '%') {
                std::string bytes;
                while (i < str.size() && str[i] == '%') {
                    if (i + 2 >= str.size() ||
                        !std::isxdigit(static_cast<unsigned char>(str[i + 1])) ||
                        !std::isxdigit(static_cast<unsigned char>(str[i + 2]))) {
                        throw std::invalid_argument("URLDecoder: Incomplete trailing escape (%) pattern");
                    }
                    bytes += static_cast<char>(hexVal(str[i + 1]) * 16 + hexVal(str[i + 2]));
                    i += 3;
                }
                result += decodeBytes(bytes, charset);
            } else {
                result += c;
                ++i;
            }
        }

        return result;
    }
};