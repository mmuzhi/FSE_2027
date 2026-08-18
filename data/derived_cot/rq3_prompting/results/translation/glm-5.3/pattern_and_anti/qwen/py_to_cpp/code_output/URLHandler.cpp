#include <map>
#include <optional>
#include <string>
#include <vector>

class URLHandler {
public:
    explicit URLHandler(std::string url) : url_(std::move(url)) {}

    std::optional<std::string> get_scheme() const {
        std::string::size_type scheme_end = url_.find("://");
        if (scheme_end != std::string::npos) {
            return url_.substr(0, scheme_end);
        }
        return std::nullopt;
    }

    std::optional<std::string> get_host() const {
        std::string::size_type scheme_end = url_.find("://");
        if (scheme_end != std::string::npos) {
            std::string url_without_scheme = url_.substr(scheme_end + 3);
            std::string::size_type host_end = url_without_scheme.find("/");
            if (host_end != std::string::npos) {
                return url_without_scheme.substr(0, host_end);
            }
            return url_without_scheme;
        }
        return std::nullopt;
    }

    std::optional<std::string> get_path() const {
        std::string::size_type scheme_end = url_.find("://");
        if (scheme_end != std::string::npos) {
            std::string url_without_scheme = url_.substr(scheme_end + 3);
            std::string::size_type host_end = url_without_scheme.find("/");
            if (host_end != std::string::npos) {
                return url_without_scheme.substr(host_end);
            }
        }
        return std::nullopt;
    }

    std::optional<std::map<std::string, std::string>> get_query_params() const {
        std::string::size_type query_start = url_.find("?");
        std::string::size_type fragment_start = url_.find("#");
        if (query_start != std::string::npos) {
            // Python: url[query_start + 1 : fragment_start]
            // Note: when fragment is absent, Python's -1 index means len(url) - 1.
            std::string::size_type start = query_start + 1;
            std::string::size_type end = (fragment_start != std::string::npos)
                                             ? fragment_start
                                             : (url_.empty() ? 0 : url_.size() - 1);
            std::string query_string =
                (start < end) ? url_.substr(start, end - start) : std::string();
            std::map<std::string, std::string> params;
            if (!query_string.empty()) {
                std::vector<std::string> param_pairs = split(query_string, '&');
                for (const std::string& pair : param_pairs) {
                    std::vector<std::string> key_value = split(pair, '=');
                    if (key_value.size() == 2) {
                        params[key_value[0]] = key_value[1];
                    }
                }
            }
            return params;
        }
        return std::nullopt;
    }

    std::optional<std::string> get_fragment() const {
        std::string::size_type fragment_start = url_.find("#");
        if (fragment_start != std::string::npos) {
            return url_.substr(fragment_start + 1);
        }
        return std::nullopt;
    }

private:
    std::string url_;

    // Equivalent of Python's str.split(sep): keeps empty parts,
    // e.g. "a&&b" -> ["a", "", "b"]; "a=" -> ["a", ""].
    static std::vector<std::string> split(const std::string& s, char sep) {
        std::vector<std::string> parts;
        std::string::size_type start = 0;
        while (true) {
            std::string::size_type pos = s.find(sep, start);
            if (pos == std::string::npos) {
                parts.push_back(s.substr(start));
                break;
            }
            parts.push_back(s.substr(start, pos - start));
            start = pos + 1;
        }
        return parts;
    }
};