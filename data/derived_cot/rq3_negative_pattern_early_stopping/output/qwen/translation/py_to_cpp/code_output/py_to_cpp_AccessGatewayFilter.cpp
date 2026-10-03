#include <iostream>
#include <unordered_map>
#include <vector>
#include <string>
#include <optional>
#include <ctime>
#include <iomanip>
#include <sstream>
#include <stdexcept>

// Define a struct for the request with path, method, and headers
struct Request {
    std::string path;
    std::string method;
    std::unordered_map<std::string, std::unordered_map<std::string, std::string>> headers;
};

class AccessGatewayFilter {
public:
    bool filter(const Request& request) {
        std::string request_uri = request.path;
        std::string method = request.method;

        if (is_start_with(request_uri)) {
            return true;
        }

        try {
            auto token = get_jwt_user(request);
            if (!token.has_value()) {
                return false;
            }
            auto& auth_header = token.value();
            auto& user_dict = auth_header["user"];
            int user_level = std::stoi(user_dict["level"]);
            if (user_level > 2) {
                set_current_user_info_and_log(user_dict);
                return true;
            }
        } catch (...) {
            return false;
        }
        return false;
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

    std::optional<std::unordered_map<std::string, std::string>> get_jwt_user(const Request& request) {
        auto& auth_headers = request.headers["Authorization"];
        auto& auth_header = auth_headers["Authorization"];
        auto& token_dict = auth_header;

        std::string jwt_token = token_dict["jwt"];
        std::string user_name = token_dict["user"]["name"];
        if (jwt_token.find(user_name) != std::string::npos) {
            std::string date_str = jwt_token.substr(user_name.size());
            std::istringstream iss(date_str);
            std::tm t = {};
            iss >> std::get_time(&t, "%Y-%m-%d");
            std::time_t date_time = std::mktime(&t);
            std::time_t current_time = std::time(nullptr);

            if (std::difftime(current_time, date_time) >= 3 * 86400) {
                return std::nullopt;
            }
        }
        return token_dict;
    }

    void set_current_user_info_and_log(const std::unordered_map<std::string, std::string>& user) {
        std::string host = user["address"];
        std::time_t now = std::time(nullptr);
        char* dt = std::asctime(std::localtime(&now));
        dt[std::strlen(dt) - 1] = '\0'; // Remove the newline
        std::cout << "DEBUG: " << user["name"] << " " << host << " " << dt << std::endl;
    }
};