#include <string>
#include <unordered_map>
#include <optional>

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
            size_t host_end = url_without_scheme.find("/");
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
            size_t host_end = url_without_scheme.find("/");
            if (host_end != std::string::npos) {
                return url_without_scheme.substr(host_end);
            }
        }
        return std::nullopt;
    }

    std::optional<std::unordered_map<std::string, std::string>> get_query_params() {
        size_t query_start = url.find("?");
        size_t fragment_start = url.find("#");
        if (query_start != std::string::npos) {
            std::string query_string;
            if (fragment_start != std::string::npos) {
                query_string = url.substr(query_start + 1, fragment_start - query_start - 1);
            } else {
                query_string = url.substr(query_start + 1);
            }
            std::unordered_map<std::string, std::string> params;
            if (!query_string.empty()) {
                size_t pos = 0;
                while (pos < query_string.size()) {
                    size_t amp_pos = query_string.find("&", pos);
                    std::string pair_str;
                    if (amp_pos != std::string::npos) {
                        pair_str = query_string.substr(pos, amp_pos - pos);
                        pos = amp_pos + 1;
                    } else {
                        pair_str = query_string.substr(pos);
                        pos = query_string.size();
                    }
                    size_t eq_pos = pair_str.find("=");
                    if (eq_pos != std::string::npos && pair_str.find("=", eq_pos + 1) == std::string::npos) {
                        std::string key = pair_str.substr(0, eq_pos);
                        std::string value = pair_str.substr(eq_pos + 1);
                        params[key] = value;
                    }
                }
            }
            return params;
        }
        return std::nullopt;
    }

    std::optional<std::string> get_fragment() {
        size_t fragment_start = url.find("#");
        if (fragment_start != std::string::npos) {
            return url.substr(fragment_start + 1);
        }
        return std::nullopt;
    }
};