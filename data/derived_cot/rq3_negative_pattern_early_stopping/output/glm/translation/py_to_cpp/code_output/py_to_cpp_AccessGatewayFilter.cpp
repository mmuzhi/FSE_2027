#include <string>
#include <vector>
#include <optional>
#include <chrono>
#include <ctime>
#include <sstream>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

class AccessGatewayFilter {
public:
    AccessGatewayFilter() {}

    std::optional<bool> filter(const json& request) {
        std::string request_uri = request["path"].get<std::string>();
        std::string method = request["method"].get<std::string>();
        (void)method;

        if (is_start_with(request_uri)) {
            return true;
        }

        try {
            auto token_opt = get_jwt_user(request);
            if (!token_opt.has_value()) {
                return false;
            }
            json token = token_opt.value();
            json user = token["user"];
            if (user["level"].get<int>() > 2) {
                set_current_user_info_and_log(user);
                return true;
            }
        } catch (...) {
            return false;
        }

        return std::nullopt;
    }

    bool is_start_with(const std::string& request_uri) {
        std::vector<std::string> start_with = {"/api", "/login"};
        for (const auto& s : start_with) {
            if (request_uri.find(s) == 0) {
                return true;
            }
        }
        return false;
    }

    std::optional<json> get_jwt_user(const json& request) {
        json token = request["headers"]["Authorization"];
        json user = token["user"];
        std::string jwt_str = token["jwt"].get<std::string>();
        std::string user_name = user["name"].get<std::string>();

        if (jwt_str.find(user_name) == 0) {
            std::vector<std::string> parts;
            size_t start = 0;
            size_t end = jwt_str.find(user_name);
            while (end != std::string::npos) {
                parts.push_back(jwt_str.substr(start, end - start));
                start = end + user_name.length();
                end = jwt_str.find(user_name, start);
            }
            parts.push_back(jwt_str.substr(start));

            std::string jwt_str_date = parts[1];

            std::tm jwt_tm = {};
            std::istringstream iss(jwt_str_date);
            iss >> std::get_time(&jwt_tm, "%Y-%m-%d");
            if (iss.fail()) {
                throw std::runtime_error("Failed to parse date");
            }

            std::time_t now_time_t = std::time(nullptr);
            std::tm now_tm = *std::localtime(&now_time_t);

            std::time_t now_t = std::mktime(&now_tm);
            std::time_t jwt_t = std::mktime(&jwt_tm);

            double diff_seconds = std::difftime(now_t, jwt_t);
            if (diff_seconds >= 3.0 * 24.0 * 60.0 * 60.0) {
                return std::nullopt;
            }
        }
        return token;
    }

    void set_current_user_info_and_log(const json& user) {
        std::string host = user["address"].get<std::string>();
        std::string name = user["name"].get<std::string>();

        auto now = std::chrono::system_clock::now();
        auto now_time_t = std::chrono::system_clock::to_time_t(now);
        std::tm now_tm = *std::localtime(&now_time_t);

        auto micros = std::chrono::duration_cast<std::chrono::microseconds>(
            now.time_since_epoch()) % 1000000;

        std::ostringstream oss;
        oss << std::put_time(&now_tm, "%Y-%m-%d %H:%M:%S")
            << "." << std::setfill('0') << std::setw(6) << micros.count();
        std::string time_str = oss.str();

        std::string msg = name + host + time_str;
        std::cerr << msg << std::endl;
    }
};