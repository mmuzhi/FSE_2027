#include <string>
#include <unordered_map>
#include <optional>
#include <fstream>
#include <stdexcept>
#include <nlohmann/json.hpp>

namespace org {
namespace example {

using CookieMap = std::unordered_map<std::string, std::string>;

class CookiesUtil {
private:
    std::string cookiesFile;
    std::optional<CookieMap> cookies;

public:
    CookiesUtil(const std::string& cookiesFile)
        : cookiesFile(cookiesFile), cookies(std::nullopt) {}

    void getCookies(const std::unordered_map<std::string, CookieMap>& response) {
        auto it = response.find("cookies");
        if (it != response.end()) {
            cookies = it->second;
        } else {
            cookies = std::nullopt;
        }
        _saveCookies();
    }

    CookieMap loadCookies() {
        std::ifstream reader(cookiesFile);
        if (!reader.is_open()) {
            return {};
        }
        nlohmann::json jsonObject;
        try {
            jsonObject = nlohmann::json::parse(reader);
        } catch (const nlohmann::json::parse_error& e) {
            return {};
        }
        
        if (!jsonObject.is_object()) {
            throw std::runtime_error("Parsed JSON is not an object");
        }

        CookieMap cookiesData;
        for (auto it = jsonObject.begin(); it != jsonObject.end(); ++it) {
            cookiesData[it.key()] = it.value().get<std::string>();
        }
        return cookiesData;
    }

    bool _saveCookies() {
        std::ofstream file(cookiesFile);
        if (!file.is_open()) {
            return false;
        }
        nlohmann::json jsonObject = nlohmann::json::object();
        if (cookies.has_value()) {
            for (const auto& kv : cookies.value()) {
                jsonObject[kv.first] = kv.second;
            }
        }
        file << jsonObject.dump();
        file.flush();
        return file.good();
    }

    void setCookies(CookieMap& request) {
        std::string cookiesString;
        if (cookies.has_value()) {
            for (const auto& kv : cookies.value()) {
                if (!cookiesString.empty()) {
                    cookiesString += "; ";
                }
                cookiesString += kv.first + "=" + kv.second;
            }
        }
        request["cookies"] = cookiesString;
    }
};

} // namespace example
} // namespace org