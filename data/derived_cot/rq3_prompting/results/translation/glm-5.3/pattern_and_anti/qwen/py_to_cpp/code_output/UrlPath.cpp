#include <string>
#include <vector>

// The class is a utility for encapsulating and manipulating the path component
// of a URL, including adding nodes, parsing path strings, and building path
// strings with optional encoding.
class UrlPath {
public:
    std::vector<std::string> segments;
    bool with_end_tag;

    // Initializes the UrlPath object with an empty list of segments and a flag
    // indicating the presence of an end tag.
    UrlPath() : with_end_tag(false) {}

    // Adds a segment to the list of segments in the UrlPath.
    void add(const std::string& segment) {
        segments.push_back(fix_path(segment));
    }

    // Parses a given path string and populates the list of segments in the UrlPath.
    // :param path: the path string to parse.
    // :param charset: the character encoding of the path string.
    void parse(const std::string& path, const std::string& charset) {
        if (!path.empty()) {
            if (path.back() == '/') {
                with_end_tag = true;
            }

            std::string fixed = fix_path(path);
            if (!fixed.empty()) {
                // split on '/', keeping empty segments (matches Python's str.split('/'))
                std::string seg;
                for (std::size_t i = 0; i < fixed.size(); ++i) {
                    if (fixed[i] == '/') {
                        segments.push_back(unquote(seg, charset));
                        seg.clear();
                    } else {
                        seg.push_back(fixed[i]);
                    }
                }
                segments.push_back(unquote(seg, charset));
            }
        }
    }

    // Fixes the given path string by removing leading and trailing slashes.
    // :param path: the path string to fix.
    // :return: the fixed path string.
    static std::string fix_path(const std::string& path) {
        if (path.empty()) {
            return "";
        }

        std::size_t start = path.find_first_not_of('/');
        if (start == std::string::npos) {
            return "";
        }
        std::size_t end = path.find_last_not_of('/');
        return path.substr(start, end - start + 1);
    }

private:
    // Percent-decodes a segment (equivalent of urllib.parse.unquote).
    // Bytes are emitted raw; for byte-transparent encodings such as "utf-8"
    // this matches Python exactly. Invalid/incomplete %XX sequences are kept as-is.
    static std::string unquote(const std::string& s, const std::string& charset) {
        (void)charset;
        std::string out;
        out.reserve(s.size());
        for (std::size_t i = 0; i < s.size(); ++i) {
            if (s[i] == '%' && i + 2 < s.size() && is_hex(s[i + 1]) && is_hex(s[i + 2])) {
                out.push_back(static_cast<char>(hex_val(s[i + 1]) * 16 + hex_val(s[i + 2])));
                i += 2;
            } else {
                out.push_back(s[i]);
            }
        }
        return out;
    }

    static bool is_hex(char c) {
        return (c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F');
    }

    static int hex_val(char c) {
        if (c >= '0' && c <= '9') return c - '0';
        if (c >= 'a' && c <= 'f') return c - 'a' + 10;
        return c - 'A' + 10;
    }
};