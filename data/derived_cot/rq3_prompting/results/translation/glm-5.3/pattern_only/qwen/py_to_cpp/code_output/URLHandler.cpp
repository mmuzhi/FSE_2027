#include <map>
#include <optional>
#include <string>
#include <vector>

class URLHandler {
public:
    explicit URLHandler(std::string url) : url_(std::move(url)) {}

    std::optional<std::string> get_scheme() const {
        std::size_t scheme_end = url_.find("://");
        if (scheme_end != std::string::npos) {
            return url_.substr(0, scheme_end);
        }
        return std::nullopt;
    }

    std::optional<std::string> get_host() const {
        std::size_t scheme_end = url_.find("://");
        if (scheme_end != std::string::npos) {
            std::string url_without_scheme = url_.substr(scheme_end + 3);
            std::size_t host_end = url_without_scheme.find('/');
            if (host_end != std::string::npos) {
                return url_without_scheme.substr(0, host_end);
            }
            return url_without_scheme;
        }
        return std::nullopt;
    }

    std::optional<std::string> get_path() const {
        std::size_t scheme_end = url_.find("://");
        if (scheme_end != std::string::npos) {
            std::string url_without_scheme = url_.substr(scheme_end + 3);
            std::size_t host_end = url_without_scheme.find('/');
            if (host_end != std::string::npos) {
                return url_without_scheme.substr(host_end);
            }
        }
        return std::nullopt;
    }

    std::optional<std::map<std::string, std::string>> get_query_params() const {
        std::size_t query_start = url_.find('?');
        std::size_t fragment_start = url_.find('#');
        if (query_start != std::string::npos) {
            std::size_t start = query_start + 1;
            // Python slice url[query_start+1 : fragment_start]: when no '#'
            // exists, fragment_start == -1 acts as negative index len-1,
            // i.e. the last character is excluded.
            std::size_t stop = (fragment_start != std::string::npos)
                                   ? fragment_start
                                   : (url_.length() - 1);
            std::string query_string;
            if (start < stop) {
                query_string = url_.substr(start, stop - start);
            }
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
        std::size_t fragment_start = url_.find('#');
        if (fragment_start != std::string::npos) {
            return url_.substr(fragment_start + 1);
        }
        return std::nullopt;
    }

private:
    std::string url_;

    static std::vector<std::string> split(const std::string& s, char delim) {
        std::vector<std::string> parts;
        std::string current;
        for (char c : s) {
            if (c == delim) {
                parts.push_back(current);
                current.clear();
            } else {
                current += c;
            }
        }
        parts.push_back(current);
        return parts;
    }
};