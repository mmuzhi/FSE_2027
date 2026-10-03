#include <string>
#include <map>
#include <optional>
#include <vector>
#include <sstream>

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

    std::optional<std::map<std::string, std::string>> getQueryParams() const {
        size_t queryStart = url.find('?');
        size_t fragmentStart = url.find('#');
        if (queryStart != std::string::npos) {
            std::string queryString = url.substr(queryStart + 1,
                (fragmentStart != std::string::npos ? fragmentStart : url.length()) - (queryStart + 1));
            std::map<std::string, std::string> params;
            if (!queryString.empty()) {
                std::vector<std::string> paramPairs;
                std::istringstream ss(queryString);
                std::string token;
                while (std::getline(ss, token, '&')) {
                    paramPairs.push_back(token);
                }
                for (const auto& pair : paramPairs) {
                    size_t eqPos = pair.find('=');
                    if (eqPos != std::string::npos) {
                        std::string key = pair.substr(0, eqPos);
                        std::string value = pair.substr(eqPos + 1);
                        params[key] = value;
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