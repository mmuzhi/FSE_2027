#include <string>
#include <vector>
#include <stdexcept>

class UrlPath {
public:
    std::vector<std::string> segments;
    bool with_end_tag;

    UrlPath() : with_end_tag(false) {}

    void add(const std::string& segment) {
        segments.push_back(fix_path(segment));
    }

    void parse(const std::string& path, const std::string& charset) {
        if (!path.empty()) {
            if (path.back() == '/') {
                with_end_tag = true;
            }
            std::string fixed = fix_path(path);
            if (!fixed.empty()) {
                std::vector<std::string> parts = split_string(fixed, '/');
                for (const auto& seg : parts) {
                    segments.push_back(unquote(seg, charset));
                }
            }
        }
    }

    static std::string fix_path(const std::string& path) {
        if (path.empty()) return "";
        size_t start = 0;
        size_t end = path.size();
        while (start < end && path[start] == '/') ++start;
        while (end > start && path[end - 1] == '/') --end;
        return path.substr(start, end - start);
    }

private:
    static std::vector<std::string> split_string(const std::string& s, char delim) {
        std::vector<std::string> tokens;
        size_t start = 0;
        size_t pos;
        while ((pos = s.find(delim, start)) != std::string::npos) {
            tokens.push_back(s.substr(start, pos - start));
            start = pos + 1;
        }
        tokens.push_back(s.substr(start));
        return tokens;
    }

    static bool iequals(const std::string& a, const std::string& b) {
        if (a.size() != b.size()) return false;
        for (size_t i = 0; i < a.size(); ++i) {
            char ca = a[i];
            char cb = b[i];
            if (ca >= 'A' && ca <= 'Z') ca = ca - 'A' + 'a';
            if (cb >= 'A' && cb <= 'Z') cb = cb - 'A' + 'a';
            if (ca != cb) return false;
        }
        return true;
    }

    static bool is_hex(char c) {
        return (c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F');
    }

    static int hex_val(char c) {
        if (c >= '0' && c <= '9') return c - '0';
        if (c >= 'a' && c <= 'f') return c - 'a' + 10;
        return c - 'A' + 10;
    }

    static std::string percent_decode(const std::string& s) {
        std::string result;
        for (size_t i = 0; i < s.size(); ++i) {
            if (s[i] == '%' && i + 2 < s.size() && is_hex(s[i + 1]) && is_hex(s[i + 2])) {
                result.push_back(static_cast<char>(hex_val(s[i + 1]) * 16 + hex_val(s[i + 2])));
                i += 2;
            } else {
                result.push_back(s[i]);
            }
        }
        return result;
    }

    static std::string utf8_replace(const std::string& input) {
        std::string output;
        const std::string replacement = "\xEF\xBF\xBD";
        size_t i = 0;
        while (i < input.size()) {
            unsigned char c = static_cast<unsigned char>(input[i]);
            if (c < 0x80) {
                output.push_back(static_cast<char>(c));
                ++i;
                continue;
            }

            size_t len;
            unsigned char min_second = 0x80, max_second = 0xBF;
            if (c >= 0xC2 && c <= 0xDF) {
                len = 2;
            } else if (c >= 0xE0 && c <= 0xEF) {
                len = 3;
                if (c == 0xE0) min_second = 0xA0;
                else if (c == 0xED) max_second = 0x9F;
            } else if (c >= 0xF0 && c <= 0xF4) {
                len = 4;
                if (c == 0xF0) min_second = 0x90;
                else if (c == 0xF4) max_second = 0x8F;
            } else {
                output += replacement;
                ++i;
                continue;
            }

            if (i + 1 >= input.size()) {
                output += replacement;
                break;
            }

            unsigned char second = static_cast<unsigned char>(input[i + 1]);
            if (second < min_second || second > max_second) {
                output += replacement;
                i += 1;
                continue;
            }

            size_t j = 2;
            while (j < len) {
                if (i + j >= input.size()) {
                    output += replacement;
                    i += j;
                    break;
                }
                unsigned char cc = static_cast<unsigned char>(input[i + j]);
                if (cc < 0x80 || cc > 0xBF) {
                    output += replacement;
                    i += j;
                    break;
                }
                ++j;
            }

            if (j == len) {
                output.append(input, i, len);
                i += len;
            }
        }
        return output;
    }

    static std::string latin1_to_utf8(const std::string& input) {
        std::string output;
        for (unsigned char c : input) {
            if (c < 0x80) {
                output.push_back(static_cast<char>(c));
            } else if (c < 0xC0) {
                output.push_back(static_cast<char>(0xC2));
                output.push_back(static_cast<char>(0x80 | (c & 0x3F)));
            } else {
                output.push_back(static_cast<char>(0xC3));
                output.push_back(static_cast<char>(0x80 | (c & 0x3F)));
            }
        }
        return output;
    }

    static std::string ascii_replace(const std::string& input) {
        std::string output;
        const std::string replacement = "\xEF\xBF\xBD";
        for (unsigned char c : input) {
            if (c < 0x80) {
                output.push_back(static_cast<char>(c));
            } else {
                output += replacement;
            }
        }
        return output;
    }

    static std::string unquote(const std::string& s, const std::string& charset) {
        std::string decoded = percent_decode(s);
        if (iequals(charset, "utf-8") || iequals(charset, "utf8")) {
            return utf8_replace(decoded);
        } else if (iequals(charset, "latin-1") || iequals(charset, "iso-8859-1") || iequals(charset, "latin1")) {
            return latin1_to_utf8(decoded);
        } else if (iequals(charset, "ascii") || iequals(charset, "us-ascii")) {
            return ascii_replace(decoded);
        } else {
            throw std::runtime_error("unknown encoding: " + charset);
        }
    }
};