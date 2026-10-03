#include <fstream>
#include <nlohmann/json.hpp>
#include <unordered_map>
#include <string>
#include <stdexcept>

class CookiesUtil {
private:
    std::string cookiesFile;
    std::unordered_map<std::string, std::string> cookies;

    bool saveCookies() {
        try {
            std::ofstream file(cookiesFile);
            if (!file.is_open()) {
                return false;
            }

            nlohmann::json json_object;
            if (cookies.empty()) {
                file << "null";
            } else {
                for (const auto& kv : cookies) {
                    json_object[kv.first] = kv.second;
                }
                file << json_object.dump(4); // Pretty print with indentation
            }
            file.flush();
            return true;
        } catch (...) {
            return false;
        }
    }

public:
    explicit CookiesUtil(const std::string& cookiesFile) : cookiesFile(cookiesFile) {}

    void getCookies(std::unordered_map<std::string, std::unordered_map<std::string, std::string>>& response) {
        if (response.find("cookies") != response.end()) {
            cookies = response["cookies"];
        }
        saveCookies();
    }

    std::unordered_map<std::string, std::string> loadCookies() {
        try {
            std::ifstream file(cookiesFile);
            if (!file.is_open()) {
                return {};
            }

            nlohmann::json json_object = nlohmann::json::parse(file);
            std::unordered_map<std::string, std::string> cookiesData;
            for (const auto& kv : json_object.items()) {
                if (kv.value().is_string()) {
                    cookiesData[kv.key()] = kv.value().get<std::string>();
                }
            }
            return cookiesData;
        } catch (...) {
            return {};
        }
    }

    void setCookies(std::unordered_map<std::string, std::string>& request) {
        std::string cookiesString;
        bool first = true;
        for (const auto& kv : cookies) {
            if (!first) {
                cookiesString += "; ";
            }
            cookiesString += kv.first + "=" + kv.second;
            first = false;
        }
        request["cookies"] = cookiesString;
    }
};