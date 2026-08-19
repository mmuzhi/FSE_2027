#include <string>
#include <vector>

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
                // split on '/', preserving empty segments (Python str.split('/'))
                size_t start = 0;
                while (true) {
                    size_t pos = fixed.find('/', start);
                    std::string seg = (pos == std::string::npos)
                                          ? fixed.substr(start)
                                          : fixed.substr(start, pos - start);
                    segments.push_back(unquote(seg, charset));
                    if (pos == std::string::npos) break;
                    start = pos + 1;
                }
            }
        }
    }

    static std::string fix_path(const std::string& path) {
        if (path.empty()) return std::string();
        // strip('/') removes ALL leading/trailing slashes
        size_t start = path.find_first_not_of('/');
        if (start == std::string::npos) return std::string();
        size_t end = path.find_last_not_of('/');
        return path.substr(start, end - start + 1);
    }

private:
    static bool is_hex_digit(char c) {
        return (c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F');
    }

    static int hex_value(char c) {
        if (c >= '0' && c <= '9') return c - '0';
        if (c >= 'a' && c <= 'f') return c - 'a' + 10;
        return c - 'A' + 10;
    }

    // Equivalent of urllib.parse.unquote for byte-transparent charsets
    // (utf-8, latin-1, etc.): decodes %XX escapes; invalid or incomplete
    // escapes are kept literally; '+' is NOT treated as space.
    static std::string unquote(const std::string& s, const std::string& charset) {
        (void)charset;  // decoded bytes map 1:1 to the result string
        std::string result;
        result.reserve(s.size());
        size_t i = 0;
        while (i < s.size()) {
            if (s[i] == '%' && i + 2 < s.size() &&
                is_hex_digit(s[i + 1]) && is_hex_digit(s[i + 2])) {
                int byte = (hex_value(s[i + 1]) << 4) | hex_value(s[i + 2]);
                result += static_cast<char>(byte);
                i += 3;
            } else {
                result += s[i];
                ++i;
            }
        }
        return result;
    }
};