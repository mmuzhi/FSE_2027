#include <map>
#include <optional>
#include <string>
#include <utility>
#include <vector>

// The class supports to handle URLs, including extracting the scheme, host,
// path, query parameters, and fragment.
class URLHandler {
public:
    std::string url;  // public attribute, like in Python

    // Initialize URLHandler's URL
    explicit URLHandler(std::string url) : url(std::move(url)) {}

    // Get the scheme of the URL.
    // Returns the scheme if "://" is present, otherwise std::nullopt (None).
    // e.g. URLHandler("https://www.baidu.com/s?wd=aaa&rsv_spt=1#page").get_scheme() == "https"
    std::optional<std::string> get_scheme() const {
        const std::string::size_type scheme_end = url.find("://");
        if (scheme_end != std::string::npos) {
            return url.substr(0, scheme_end);  // url[:scheme_end]
        }
        return std::nullopt;
    }

    // Get the second part of the URL, which is the host domain name.
    // e.g. get_host() == "www.baidu.com"
    std::optional<std::string> get_host() const {
        const std::string::size_type scheme_end = url.find("://");
        if (scheme_end != std::string::npos) {
            const std::string url_without_scheme = url.substr(scheme_end + 3);
            const std::string::size_type host_end = url_without_scheme.find("/");
            if (host_end != std::string::npos) {
                return url_without_scheme.substr(0, host_end);
            }
            return url_without_scheme;
        }
        return std::nullopt;
    }

    // Get the third part of the URL, which is the address of the resource.
    // e.g. get_path() == "/s?wd=aaa&rsv_spt=1#page"
    std::optional<std::string> get_path() const {
        const std::string::size_type scheme_end = url.find("://");
        if (scheme_end != std::string::npos) {
            const std::string url_without_scheme = url.substr(scheme_end + 3);
            const std::string::size_type host_end = url_without_scheme.find("/");
            if (host_end != std::string::npos) {
                return url_without_scheme.substr(host_end);  // [host_end:]
            }
        }
        return std::nullopt;
    }

    // Get the request parameters for the URL.
    // Returns a map of the request parameters if a '?' is present,
    // otherwise std::nullopt (None).
    // e.g. get_query_params() == {"wd": "aaa", "rsv_spt": "1"}
    std::optional<std::map<std::string, std::string>> get_query_params() const {
        const std::string::size_type query_start = url.find("?");
        const std::string::size_type fragment_start = url.find("#");
        if (query_start != std::string::npos) {
            // Python: query_string = self.url[query_start + 1 : fragment_start]
            // When there is no '#', fragment_start is -1 in Python, and as a
            // slice bound -1 means len(url) - 1 (the last character is excluded).
            const std::string query_string = py_slice(
                url,
                static_cast<long long>(query_start) + 1,
                fragment_start == std::string::npos
                    ? -1
                    : static_cast<long long>(fragment_start));
            std::map<std::string, std::string> params;
            if (!query_string.empty()) {
                const std::vector<std::string> param_pairs = py_split(query_string, "&");
                for (const std::string& pair : param_pairs) {
                    const std::vector<std::string> key_value = py_split(pair, "=");
                    if (key_value.size() == 2) {
                        params[key_value[0]] = key_value[1];
                    }
                }
            }
            return params;
        }
        return std::nullopt;
    }

    // Get the fragment after '#' in the URL.
    // e.g. get_fragment() == "page"
    std::optional<std::string> get_fragment() const {
        const std::string::size_type fragment_start = url.find("#");
        if (fragment_start != std::string::npos) {
            return url.substr(fragment_start + 1);  // [fragment_start + 1:]
        }
        return std::nullopt;
    }

private:
    // Equivalent of Python's s[start:stop]; a negative stop (e.g. -1) has
    // len(s) added to it, exactly like Python slice indices.
    static std::string py_slice(const std::string& s, long long start, long long stop) {
        const long long len = static_cast<long long>(s.length());
        if (start < 0) start += len;
        if (stop < 0) stop += len;
        if (start < 0) start = 0;
        if (stop < 0) stop = 0;
        if (start > len) start = len;
        if (stop > len) stop = len;
        if (start >= stop) return std::string();
        return s.substr(static_cast<std::size_t>(start),
                        static_cast<std::size_t>(stop - start));
    }

    // Equivalent of Python's s.split(sep) for a non-empty separator.
    static std::vector<std::string> py_split(const std::string& s, const std::string& sep) {
        std::vector<std::string> parts;
        std::string::size_type start = 0;
        std::string::size_type pos;
        while ((pos = s.find(sep, start)) != std::string::npos) {
            parts.push_back(s.substr(start, pos - start));
            start = pos + sep.length();
        }
        parts.push_back(s.substr(start));
        return parts;
    }
};