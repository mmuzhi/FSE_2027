#include <string>
#include <optional>
#include <unordered_map>

class URLHandler {
private:
    std::string url;

public:
    URLHandler(const std::string& url) : url(url) {}

    std::optional<std::string> getScheme() const {
        size_t schemeEnd = url.find("://");
        if (schemeEnd != std::string::npos) {
            return url.substr(0, schemeEnd);
        }
        return std::nullopt;
    }

    std::optional<std::string> getHost() const {
        size_t schemeEnd = url.find("://");
        if (schemeEnd != std::string::npos) {
            std::string urlWithoutScheme = url.substr(schemeEnd + 3);
            size_t hostEnd = urlWithoutScheme.find('/');
            if (hostEnd != std::string::npos) {
                return urlWithoutScheme.substr(0, hostEnd);
            }
            return urlWithoutScheme;
        }
        return std::nullopt;
    }

    std::optional<std::string> getPath() const {
        size_t schemeEnd = url.find("://");
        if (schemeEnd != std::string::npos) {
            std::string urlWithoutScheme = url.substr(schemeEnd + 3);
            size_t hostEnd = urlWithoutScheme.find('/');
            if (hostEnd != std::string::npos) {
                return urlWithoutScheme.substr(hostEnd);
            }
        }
        return std::nullopt;
    }

    std::optional<std::unordered_map<std::string, std::string>> getQueryParams() const {
        size_t queryStart = url.find('?');
        size_t fragmentStart = url.find('#');
        if (queryStart != std::string::npos) {
            size_t queryEnd = (fragmentStart != std::string::npos) ? fragmentStart : url.length();
            std::string queryString = url.substr(queryStart + 1, queryEnd - (queryStart + 1));
            std::unordered_map<std::string, std::string> params;
            if (!queryString.empty()) {
                size_t start = 0;
                while (start < queryString.length()) {
                    size_t end = queryString.find('&', start);
                    if (end == std::string::npos) {
                        end = queryString.length();
                    }
                    std::string pair = queryString.substr(start, end - start);
                    size_t equalPos = pair.find('=');
                    if (equalPos != std::string::npos && equalPos < pair.length() - 1) {
                        std::string key = pair.substr(0, equalPos);
                        std::string value = pair.substr(equalPos + 1);
                        params[key] = value;
                    }
                    start = end + 1;
                }
            }
            return params;
        }
        return std::nullopt;
    }

    std::optional<std::string> getFragment() const {
        size_t fragmentStart = url.find('#');
        if (fragmentStart != std::string::npos) {
            return url.substr(fragmentStart + 1);
        }
        return std::nullopt;
    }
};