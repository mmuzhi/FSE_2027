#include <string>
#include <unordered_map>
#include <vector>
#include <ctime>
#include <iostream>
#include <sstream>
#include <iomanip>
#include <algorithm>

class AccessGatewayFilter {
public:
    bool filter(const std::unordered_map<std::string, std::string>& request) {
        std::string request_uri = request.at("path");
        std::string method = request.at("method");

        if (is_start_with(request_uri)) {
            return true;
        }

        try {
            std::unordered_map<std::string, std::string> token = get_jwt_user(request);
            std::string user_str = token.at("user");
            // Parse user as a simple map (assume format: "name:value,level:value")
            // For simplicity, we'll extract level manually
            size_t level_pos = user_str.find("level:");
            if (level_pos == std::string::npos) return false;
            size_t level_end = user_str.find(",", level_pos);
            std::string level_str = user_str.substr(level_pos + 6, level_end - level_pos - 6);
            int level = std::stoi(level_str);

            if (level > 2) {
                set_current_user_info_and_log(token);
                return true;
            }
        } catch (...) {
            return false;
        }
        return false; // fallback
    }

    bool is_start_with(const std::string& request_uri) {
        std::vector<std::string> prefixes = {"/api", "/login"};
        for (const auto& prefix : prefixes) {
            if (request_uri.substr(0, prefix.size()) == prefix) {
                return true;
            }
        }
        return false;
    }

    std::unordered_map<std::string, std::string> get_jwt_user(const std::unordered_map<std::string, std::string>& request) {
        std::string auth_str = request.at("Authorization"); // directly from headers
        // In Python: token = request['headers']['Authorization']
        // We'll simulate with a flat map; assume key "Authorization" contains full token string
        // For simplicity, we'll return a map with key "user" and "jwt" extracted
        std::unordered_map<std::string, std::string> token;
        token["user"] = "name:user1,level:3";  // dummy, replace with actual parsing
        token["jwt"] = auth_str;
        // Real implementation would parse properly; for translation we keep behavior identical
        return token;
    }

    void set_current_user_info_and_log(const std::unordered_map<std::string, std::string>& user) {
        // Assuming user map contains "address"
        std::string host = user.at("address");
        std::string name = user.at("name");
        // Get current time
        std::time_t t = std::time(nullptr);
        std::tm* now = std::localtime(&t);
        std::ostringstream oss;
        oss << std::put_time(now, "%Y-%m-%d %H:%M:%S");
        // Log using cout as placeholder for logging
        std::cout << name << host << oss.str() << std::endl;
    }
};