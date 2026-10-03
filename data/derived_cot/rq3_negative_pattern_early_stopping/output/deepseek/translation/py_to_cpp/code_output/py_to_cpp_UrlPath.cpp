#include <string>
#include <vector>
#include <algorithm>
#include <sstream>
#include <cstdlib>

class UrlPath {
public:
    std::vector<std::string> segments;
    bool with_end_tag = false;

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
                std::stringstream ss(fixed);
                std::string segment;
                while (std::getline(ss, segment, '/')) {
                    segments.push_back(url_decode(segment, charset));
                }
            }
        }
    }

    static std::string fix_path(const std::string& path) {
        if (path.empty()) {
            return "";
        }

        size_t start = 0;
        size_t end = path.length();
        while (start < end && path[start] == '/') {
            ++start;
        }
        while (end > start && path[end - 1] == '/') {
            --end;
        }
        return path.substr(start, end - start);
    }

private:
    static std::string url_decode(const std::string& encoded, const std::string& charset) {
        std::string decoded;
        size_t i = 0;
        while (i < encoded.length()) {
            if (encoded[i] == '%' && i + 2 < encoded.length()) {
                std::string hex = encoded.substr(i + 1, 2);
                char* end;
                long code = std::strtol(hex.c_str(), &end, 16);
                if (*end == '\0') {
                    decoded.push_back(static_cast<char>(code));
                    i += 3;
                    continue;
                }
            }
            decoded.push_back(encoded[i]);
            ++i;
        }

        // If charset is not "utf-8", we need to handle it differently,
        // but for exact behavior, we assume the decoded bytes are interpreted
        // with the given charset. In C++, we treat the bytes as-is.
        // The charset parameter is ignored here for simplicity, but we include it
        // to match the interface. To fully implement charset decoding would require
        // a conversion library. This matches behavior when charset is "utf-8" or
        // when the decoded bytes form valid Latin-1 etc., but Python's unquote
        // returns a string decoded from bytes. For most common ASCII/UTF-8 usage,
        // the above works. For other charsets, the result may differ slightly.
        // We note that the charset parameter is accepted but not used, akin to
        // a common C++ simplification.
        (void)charset; // suppress unused warning
        return decoded;
    }
};