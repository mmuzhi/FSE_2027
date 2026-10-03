#include <string>
#include <optional>
#include <vector>
#include <sstream>
#include <map>

class URLHandler {
private:
    std::string url;

public:
    URLHandler(const std::string& url) : url(url) {}

    std::optional<std::string> get_scheme() {
        size_t scheme_end = url.find("://");
        if (scheme_end != std::string::npos) {
            return url.substr(0, scheme_end);
        }
        return std::nullopt;
    }

    std::optional<std::string> get_host() {
        size_t scheme_end = url.find("://");
        if (scheme_end != std::string::npos) {
            std::string url_without_scheme = url.substr(scheme_end + 3);
            size_t host_end = url_without_scheme.find('/');
            if (host_end != std::string::npos) {
                return url_without_scheme.substr(0, host_end);
            }
            return url_without_scheme;
        }
        return std::nullopt;
    }

    std::optional<std::string> get_path() {
        size_t scheme_end = url.find("://");
        if (scheme_end != std::string::npos) {
            std::string url_without_scheme = url.substr(scheme_end + 3);
            size_t host_end = url_without_scheme.find('/');
            if (host_end != std::string::npos) {
                return url_without_scheme.substr(host_end);
            }
            return url_without_scheme;
        }
        return std::nullopt;
    }

    std::optional<std::map<std::string, std::string>> get_query_params() {
        size_t query_start = url.find('?');
        size_t fragment_start = url.find('#');
        if (query_start != std::string::npos) {
            std::string query_string;
            if (fragment_start != std::string::npos) {
                query_string = url.substr(query_start + 1, fragment_start - (query_start + 1));
            } else {
                query_string = url.substr(query_start + 1);
            }

            if (!query_string.empty()) {
                std::map<std::string, std::string> params;
                std::istringstream iss(query_string);
                std::string pair;
                while (std::getline(iss, pair, '&')) {
                    size_t eq_pos = pair.find('=');
                    if (eq_pos != std::string::npos) {
                        std::string key = pair.substr(0, eq_pos);
                        std::string value = pair.substr(eq_pos + 1);
                        params[key] = value;
                    } else {
                        // If there's no '=', then treat the whole pair as key and empty value?
                        params[pair] = "";
                    }
                }
                return params;
            }
            return std::map<std::string, std::string>();
        }
        return std::nullopt;
    }

    std::optional<std::string> get_fragment() {
        size_t fragment_start = url.find('#');
        if (fragment_start != std::string::npos) {
            return url.substr(fragment_start + 1);
        }
        return std::nullopt;
    }
};