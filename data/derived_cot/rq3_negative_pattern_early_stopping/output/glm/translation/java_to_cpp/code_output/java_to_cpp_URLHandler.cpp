#include <string>
#include <unordered_map>
#include <optional>
#include <vector>

class URLHandler {
private:
    std::string url;

    std::vector<std::string> split(const std::string& s, char delim) const {
        std::vector<std::string> tokens;
        size_t start = 0;
        size_t end = s.find(delim);
        while (end != std::string::npos) {
            tokens.push_back(s.substr(start, end - start));
            start = end + 1;
            end = s.find(delim, start);
        }
        tokens.push_back(s.substr(start));
        while (!tokens.empty() && tokens.back().empty()) {
            tokens.pop_back();
        }
        return tokens;
    }

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
            std::string queryString;
            if (fragmentStart != std::string::npos) {
                queryString = url.substr(queryStart + 1, fragmentStart - queryStart - 1);
            } else {
                queryString = url.substr(queryStart + 1);
            }
            
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
        size_t fragmentStart = url.find('#');
        if (fragmentStart != std::string::npos) {
            return url.substr(fragmentStart + 1);
        }
        return std::nullopt;
    }
};