#include <cstddef>
#include <optional>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace org::example {

class URLHandler {
private:
    std::string url;

    // Mirrors Java's String.substring(begin, end):
    // throws if begin > end or end > length (StringIndexOutOfBoundsException analog).
    static std::string substring(const std::string& s, std::size_t begin, std::size_t end) {
        if (begin > end || end > s.size()) {
            throw std::out_of_range("begin " + std::to_string(begin) +
                                    ", end " + std::to_string(end) +
                                    ", length " + std::to_string(s.size()));
        }
        return s.substr(begin, end - begin);
    }

    // Mirrors Java's String.split(delim) with limit 0:
    // trailing empty strings are discarded.
    static std::vector<std::string> split(const std::string& s, char delim) {
        std::vector<std::string> parts;
        std::string cur;
        for (char c : s) {
            if (c == delim) {
                parts.push_back(cur);
                cur.clear();
            } else {
                cur.push_back(c);
            }
        }
        parts.push_back(cur);
        while (!parts.empty() && parts.back().empty()) {
            parts.pop_back();
        }
        return parts;
    }

public:
    explicit URLHandler(std::string url) : url(std::move(url)) {}

    // Java returns null when absent -> std::nullopt.
    std::optional<std::string> getScheme() const {
        std::size_t schemeEnd = url.find("://");
        if (schemeEnd != std::string::npos) {
            return url.substr(0, schemeEnd);
        }
        return std::nullopt;
    }

    std::optional<std::string> getHost() const {
        std::size_t schemeEnd = url.find("://");
        if (schemeEnd != std::string::npos) {
            std::string urlWithoutScheme = url.substr(schemeEnd + 3);
            std::size_t hostEnd = urlWithoutScheme.find('/');
            if (hostEnd != std::string::npos) {
                return urlWithoutScheme.substr(0, hostEnd);
            }
            return urlWithoutScheme;
        }
        return std::nullopt;
    }

    std::optional<std::string> getPath() const {
        std::size_t schemeEnd = url.find("://");
        if (schemeEnd != std::string::npos) {
            std::string urlWithoutScheme = url.substr(schemeEnd + 3);
            std::size_t hostEnd = urlWithoutScheme.find('/');
            if (hostEnd != std::string::npos) {
                return urlWithoutScheme.substr(hostEnd);
            }
        }
        return std::nullopt;
    }

    std::optional<std::unordered_map<std::string, std::string>> getQueryParams() const {
        std::size_t queryStart = url.find('?');
        std::size_t fragmentStart = url.find('#');
        if (queryStart != std::string::npos) {
            std::size_t end = (fragmentStart != std::string::npos) ? fragmentStart : url.size();
            std::string queryString = substring(url, queryStart + 1, end);
            std::unordered_map<std::string, std::string> params;
            if (!queryString.empty()) {
                std::vector<std::string> paramPairs = split(queryString, '&');
                for (const std::string& pair : paramPairs) {
                    std::vector<std::string> keyValue = split(pair, '=');
                    if (keyValue.size() == 2) {
                        params[keyValue[0]] = keyValue[1];
                    }
                }
            }
            return params;
        }
        return std::nullopt;
    }

    std::optional<std::string> getFragment() const {
        std::size_t fragmentStart = url.find('#');
        if (fragmentStart != std::string::npos) {
            return url.substr(fragmentStart + 1);
        }
        return std::nullopt;
    }
};

} // namespace org::example