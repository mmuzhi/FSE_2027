#include <optional>
#include <map>
#include <string>

class URLHandler {
private:
    std::string url;

public:
    URLHandler(const std::string& url) : url(url) {}

    std::optional<std::string> get_scheme() const {
        size_t scheme_end = url.find("://");
        if (scheme_end != std::string::npos) {
            return url.substr(0, scheme_end);
        }
        return std::nullopt;
    }

    std::optional<std::string> get_host() const {
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

    std::optional<std::string> get_path() const {
        size_t scheme_end = url.find("://");
        if (scheme_end != std::string::npos) {
            std::string url_without_scheme = url.substr(scheme_end + 3);
            size_t host_end = url_without_scheme.find('/');
            if (host_end != std::string::npos) {
                return url_without_scheme.substr(host_end);
            }
        }
        return std::nullopt;
    }

    std::optional<std::map<std::string, std::string>> get_query_params() const {
        size_t query_start = url.find('?');
        size_t fragment_start = url.find('#');

        if (query_start != std::string::npos) {
            size_t start = query_start + 1;
            size_t end;
            if (fragment_start == std::string::npos) {
                end = url.length() - 1;
            } else {
                end = fragment_start;
            }

            std::string query_string;
            if (start < end) {
                query_string = url.substr(start, end - start);
            }

            std::map<std::string, std::string> params;
            if (!query_string.empty()) {
                size_t pos = 0;
                while (pos <= query_string.length()) {
                    size_t amp = query_string.find('&', pos);
                    std::string pair;
                    bool last = false;

                    if (amp == std::string::npos) {
                        pair = query_string.substr(pos);
                        last = true;
                    } else {
                        pair = query_string.substr(pos, amp - pos);
                    }

                    size_t eq = pair.find('=');
                    if (eq != std::string::npos) {
                        size_t eq2 = pair.find('=', eq + 1);
                        if (eq2 == std::string::npos) {
                            params[pair.substr(0, eq)] = pair.substr(eq + 1);
                        }
                    }

                    if (last) break;
                    pos = amp + 1;
                }
            }

            return params;
        }

        return std::nullopt;
    }

    std::optional<std::string> get_fragment() const {
        size_t fragment_start = url.find('#');
        if (fragment_start != std::string::npos) {
            return url.substr(fragment_start + 1);
        }
        return std::nullopt;
    }
};