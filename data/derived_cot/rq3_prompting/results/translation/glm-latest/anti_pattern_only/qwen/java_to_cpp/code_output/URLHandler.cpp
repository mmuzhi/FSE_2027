#include <cstddef>
#include <optional>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

class URLHandler {
public:
    explicit URLHandler(std::string url) : url(std::move(url)) {}

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
            std::size_t beginIndex = queryStart + 1;
            std::size_t endIndex = (fragmentStart != std::string::npos) ? fragmentStart : url.length();
            if (beginIndex > endIndex) {
                // Mirrors Java's StringIndexOutOfBoundsException from substring(begin, end)
                throw std::out_of_range("beginIndex > endIndex");
            }
            std::string queryString = url.substr(beginIndex, endIndex - beginIndex);
            std::unordered_map<std::string, std::string> params;
            if (!queryString.empty()) {
                std::vector<std::string> paramPairs = javaSplit(queryString, '&');
                for (const std::string& pair : paramPairs) {
                    std::vector<std::string> keyValue = javaSplit(pair, '=');
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

private:
    std::string url;

    // Replicates Java's String.split for a single-character literal delimiter:
    // splits on every occurrence, then discards trailing empty tokens.
    static std::vector<std::string> javaSplit(const std::string& str, char delim) {
        std::vector<std::string> parts;
        std::size_t start = 0;
        while (true) {
            std::size_t pos = str.find(delim, start);
            if (pos == std::string::npos) {
                parts.push_back(str.substr(start));
                break;
            }
            parts.push_back(str.substr(start, pos - start));
            start = pos + 1;
        }
        while (!parts.empty() && parts.back().empty()) {
            parts.pop_back();
        }
        return parts;
    }
};