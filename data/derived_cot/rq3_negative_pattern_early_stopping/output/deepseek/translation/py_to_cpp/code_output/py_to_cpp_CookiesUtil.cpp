#include <string>
#include <fstream>
#include <optional>
#include <filesystem>
#include <nlohmann/json.hpp>

namespace fs = std::filesystem;
using json = nlohmann::json;

class CookiesUtil {
private:
    std::string cookies_file;
    std::optional<json> cookies;

public:
    CookiesUtil(const std::string& file) : cookies_file(file), cookies(std::nullopt) {}

    void get_cookies(json& response) {
        // If response does not contain "cookies", this throws (like Python KeyError).
        cookies = response["cookies"];
        _save_cookies();
    }

    json load_cookies() {
        // If the file does not exist, return an empty object (like Python's FileNotFoundError catch).
        if (!fs::exists(cookies_file)) {
            return json::object();
        }
        std::ifstream file(cookies_file);
        if (!file.is_open()) {
            // File exists but cannot be opened -> propagate exception (Python would raise PermissionError).
            throw std::runtime_error("Cannot open cookies file: " + cookies_file);
        }
        json cookies_data;
        file >> cookies_data;           // throws on parse error (like Python's JSONDecodeError)
        return cookies_data;
    }

    bool _save_cookies() {
        std::ofstream file(cookies_file);
        if (!file.is_open()) {
            return false;
        }
        try {
            // If cookies is std::nullopt, we write null (same as Python's json.dump(None)).
            file << cookies.value_or(json()) << std::endl;
            return true;
        } catch (...) {
            return false;
        }
    }

    void set_cookies(json& request) {
        // This will throw std::bad_optional_access if cookies is nullopt,
        // analogous to Python's AttributeError (None has no attribute 'items').
        std::string cookies_str;
        bool first = true;
        for (auto& [key, value] : cookies.value().items()) {
            if (!first) cookies_str += "; ";
            cookies_str += key + "=" + value.get<std::string>();
            first = false;
        }
        request["cookies"] = cookies_str;
    }
};