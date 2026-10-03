#include <fstream>
#include <string>
#include <map>
#include <json/json.h> // Include the JSON library (e.g., nlohmann/json)

class CookiesUtil {
private:
    std::string cookies_file;
    std::map<std::string, std::string> cookies;

    bool save_cookies() {
        try {
            std::ofstream file(cookies_file);
            if (file.is_open()) {
                json j;
                for (const auto& pair : cookies) {
                    j[pair.first] = pair.second;
                }
                file << j.dump(4); // Pretty print JSON
                file.close();
                return true;
            }
        } catch (...) {
            return false;
        }
        return false;
    }

public:
    CookiesUtil(const std::string& cookies_file) : cookies_file(cookies_file) {}

    void get_cookies(const json& response) {
        if (response.contains("cookies") && response["cookies"].is_object()) {
            const auto& response_cookies = response["cookies"];
            for (const auto& pair : response_cookies.items()) {
                cookies[pair.first] = pair.second;
            }
            save_cookies();
        }
    }

    json load_cookies() {
        try {
            std::ifstream file(cookies_file);
            if (file.is_open()) {
                json j = json::parse(file);
                for (const auto& pair : j.items()) {
                    cookies[pair.first] = pair.second;
                }
                return j;
            }
        } catch (...) {
            return json{}; // Return empty JSON object on error
        }
        return json{}; // Return empty JSON object if no cookies
    }

    void set_cookies(json& request) {
        std::string cookie_string;
        for (const auto& pair : cookies) {
            if (!cookie_string.empty()) {
                cookie_string += "; ";
            }
            cookie_string += pair.first + "=" + pair.second;
        }
        request["cookies"] = cookie_string;
    }
};