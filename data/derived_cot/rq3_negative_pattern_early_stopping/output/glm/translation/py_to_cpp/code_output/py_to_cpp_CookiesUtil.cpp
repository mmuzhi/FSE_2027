#include <nlohmann/json.hpp>
#include <fstream>
#include <string>
#include <optional>

using json = nlohmann::json;

class CookiesUtil {
public:
    std::string cookies_file;
    std::optional<json> cookies;

    CookiesUtil(const std::string& cookies_file)
        : cookies_file(cookies_file), cookies(std::nullopt) {}

    void get_cookies(const json& response) {
        cookies = response["cookies"];
        _save_cookies();
    }

    json load_cookies() {
        std::ifstream file(cookies_file);
        if (!file.is_open()) {
            return json::object();
        }
        json cookies_data = json::parse(file);
        return cookies_data;
    }

    bool _save_cookies() {
        try {
            std::ofstream file(cookies_file);
            if (!file.is_open()) {
                return false;
            }
            file << cookies->dump();
            return true;
        } catch (...) {
            return false;
        }
    }

    void set_cookies(json& request) {
        std::string result;
        bool first = true;
        for (auto& [key, value] : cookies->items()) {
            if (!first) {
                result += "; ";
            }
            result += key + "=" + value.get<std::string>();
            first = false;
        }
        request["cookies"] = result;
    }
};