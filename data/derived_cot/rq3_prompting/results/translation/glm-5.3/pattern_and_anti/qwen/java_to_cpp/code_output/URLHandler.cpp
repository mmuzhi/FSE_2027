#include <string>
#include <vector>
#include <optional>
#include <unordered_map>
#include <stdexcept>
#include <cstddef>
#include <utility>

namespace org::example {

class URLHandler {
private:
    std::string url;

    // Mirrors Java String.substring(begin, end): throws when begin > end,
    // begin < 0, or end > length (Java: StringIndexOutOfBoundsException).
    static std::string substring(const std::string& s, std::ptrdiff_t begin, std::ptrdiff_t end) {
        if (begin < 0 || end > static_cast<std::ptrdiff_t>(s.size()) || begin > end) {
            throw std::out_of_range("begin " + std::to_string(begin) +
                                    ", end " + std::to_string(end) +
                                    ", length " + std::to_string(s.size()));
        }
        return s.substr(static_cast<std::size_t>(begin),
                        static_cast<std::size_t>(end - begin));
    }

    static std::string substring(const std::string& s, std::ptrdiff_t begin) {
        if (begin < 0 || begin > static_cast<std::ptrdiff_t>(s.size())) {
            throw std::out_of_range("begin " + std::to_string(begin) +
                                    ", length " + std::to_string(s.size()));
        }
        return s.substr(static_cast<std::size_t>(begin));
    }

    // Mirrors Java String.split with a single-char delimiter and limit 0:
    // leading/middle empty segments are kept, trailing empty segments removed.
    static std::vector<std::string> javaSplit(const std::string& s, char delim) {
        std::vector<std::string> parts;
        std::string cur;
        for (char c : s) {
            if (c == delim) {
                parts.push_back(cur);
                cur.clear();
            } else {
                cur += c;
            }
        }
        parts.push_back(cur);
        while (!parts.empty() && parts.back().empty()) {
            parts.pop_back();
        }
        return parts;
    }

    // Java indexOf returns -1 when not found.
    static std::ptrdiff_t indexOf(const std::string& s, const char* needle) {
        std::size_t pos = s.find(needle);
        return pos == std::string::npos ? -1 : static_cast<std::ptrdiff_t>(pos);
    }

public:
    explicit URLHandler(std::string url_) : url(std::move(url_)) {}

    // Java returns null when not found -> std::optional models that.
    std::optional<std::string> getScheme() const {
        std::ptrdiff_t schemeEnd = indexOf(url, "://");
        if (schemeEnd != -1) {
            return substring(url, 0, schemeEnd);
        }
        return std::nullopt;
    }

    std::optional<std::string> getHost() const {
        std::ptrdiff_t schemeEnd = indexOf(url, "://");
        if (schemeEnd != -1) {
            std::string urlWithoutScheme = substring(url, schemeEnd + 3);
            std::ptrdiff_t hostEnd = indexOf(urlWithoutScheme, "/");
            if (hostEnd != -1) {
                return substring(urlWithoutScheme, 0, hostEnd);
            }
            return urlWithoutScheme;
        }
        return std::nullopt;
    }

    std::optional<std::string> getPath() const {
        std::ptrdiff_t schemeEnd = indexOf(url, "://");
        if (schemeEnd != -1) {
            std::string urlWithoutScheme = substring(url, schemeEnd + 3);
            std::ptrdiff_t hostEnd = indexOf(urlWithoutScheme, "/");
            if (hostEnd != -1) {
                return substring(urlWithoutScheme, hostEnd);
            }
        }
        return std::nullopt;
    }

    std::optional<std::unordered_map<std::string, std::string>> getQueryParams() const {
        std::ptrdiff_t queryStart = indexOf(url, "?");
        std::ptrdiff_t fragmentStart = indexOf(url, "#");
        if (queryStart != -1) {
            // Note: if fragmentStart < queryStart + 1, Java's substring throws;
            // the helper above reproduces that (std::out_of_range).
            std::string queryString = substring(
                url, queryStart + 1,
                fragmentStart != -1 ? fragmentStart : static_cast<std::ptrdiff_t>(url.size()));
            std::unordered_map<std::string, std::string> params;
            if (!queryString.empty()) {
                std::vector<std::string> paramPairs = javaSplit(queryString, '&');
                for (const std::string& pair : paramPairs) {
                    std::vector<std::string> keyValue = javaSplit(pair, '=');
                    if (keyValue.size() == 2) {
                        params[keyValue[0]] = keyValue[1]; // put: last value wins
                    }
                }
            }
            return params;
        }
        return std::nullopt;
    }

    std::optional<std::string> getFragment() const {
        std::ptrdiff_t fragmentStart = indexOf(url, "#");
        if (fragmentStart != -1) {
            return substring(url, fragmentStart + 1);
        }
        return std::nullopt;
    }
};

} // namespace org::example