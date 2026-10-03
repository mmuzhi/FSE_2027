#include <string>
#include <map>
#include <fstream>
#include <nlohmann/json.hpp>
#include <optional>

using json = nlohmann::json;

class CookiesUtil {
private:
    std::string cookiesFile;
    std::optional<std::map<std::string, std::string>> cookies;

public:
    CookiesUtil(const std::string& cookiesFile)
        : cookiesFile(cookiesFile), cookies(std::nullopt) {}

    // Mimics Java's getCookies(Map<String, Map<String, String>> response)
    void getCookies(std::map<std::string, std::map<std::string, std::string>>& response) {
        auto it = response.find("cookies");
        if (it != response.end()) {
            cookies = it->second;           // copy the inner map
        } else {
            cookies = std::nullopt;
        }
        _saveCookies();                     // always save after retrieving
    }

    // Mimics Java's loadCookies()
    std::map<std::string, std::string> loadCookies() {
        json j;
        try {
            std::ifstream file(cookiesFile);
            if (!file.is_open()) {
                return {};
            }
            file >> j;
            std::map<std::string, std::string> result;
            for (auto it = j.begin(); it != j.end(); ++it) {
                result[it.key()] = it.value().get<std::string>();
            }
            return result;
        } catch (...) {
            return {};
        }
    }

    // Mimics Java's _saveCookies()
    bool _saveCookies() {
        json j;
        if (cookies.has_value()) {
            for (const auto& [key, value] : cookies.value()) {
                j[key] = value;
            }
        }
        try {
            std::ofstream file(cookiesFile);
            if (!file.is_open()) {
                return false;
            }
            file << j.dump();      // compact JSON, like Java's toJSONString()
            file.flush();
            return true;
        } catch (...) {
            return false;
        }
    }

    // Mimics Java's setCookies(Map<String, String> request)
    void setCookies(std::map<std::string, std::string>& request) {
        std::string cookiesString;
        if (cookies.has_value()) {
            bool first = true;
            for (const auto& [key, value] : cookies.value()) {
                if (!first) {
                    cookiesString += "; ";
                }
                first = false;
                cookiesString += key + "=" + value;
            }
        }
        request["cookies"] = cookiesString;
    }
};