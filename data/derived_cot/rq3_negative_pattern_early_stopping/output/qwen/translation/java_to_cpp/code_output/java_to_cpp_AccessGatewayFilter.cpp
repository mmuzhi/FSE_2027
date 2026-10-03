#include <iostream>
#include <map>
#include <string>
#include <any>
#include <vector>
#include <cctype>
#include <exception>
#include <optional>
#include <locale>
#include <iomanip>
#include <sstream>
#include <algorithm>
#include <cctype>
#include <cstdlib>
#include <ctime>
#include <stdexcept>
#include <date/date.h>

namespace date = std::chrono;

// Helper function to convert a string to a date (yyyy-MM-dd)
std::optional<date::sys_days> parse_date(const std::string& date_str) {
    try {
        std::istringstream ss(date_str);
        date::year_month_day ymd;
        ss >> date::parse("%F", date_str.begin(), date_str.end(), ymd);
        return date::sys_days{date::year{ymd.year}, date::month{ymd.month}, date::day{ymd.day}};
    } catch (...) {
        return std::nullopt;
    }
}

class AccessGatewayFilter {
public:
    AccessGatewayFilter() = default;

    bool filter(const std::map<std::string, std::any>& request) {
        try {
            std::string requestUri = std::any_cast<std::string>(request.at("path"));
            std::string method = std::any_cast<std::string>(request.at("method"));

            if (isStartWith(requestUri)) {
                return true;
            }

            auto token = getJwtUser(request);
            if (!token) {
                return false;
            }

            auto userMap = std::any_cast<std::map<std::string, std::any>>(token.value().at("user"));
            int level = std::any_cast<int>(userMap.at("level"));

            if (level > 2) {
                setCurrentUserInfoAndLog(userMap);
                return true;
            }
        } catch (const std::exception& e) {
            return false;
        }
        return false;
    }

    bool isStartWith(const std::string& requestUri) {
        std::vector<std::string> startWith = {"/api", "/login"};
        for (const auto& s : startWith) {
            if (requestUri.substr(0, s.size()) == s) {
                return true;
            }
        }
        return false;
    }

    std::optional<std::map<std::string, std::any>> getJwtUser(const std::map<std::string, std::any>& request) {
        try {
            std::string headersKey = "headers";
            if (request.find(headersKey) == request.end()) {
                return std::nullopt;
            }
            auto headers = std::any_cast<std::map<std::string, std::any>>(request.at(headersKey));

            std::string authKey = "Authorization";
            if (headers.find(authKey) == headers.end()) {
                return std::nullopt;
            }
            auto auth = std::any_cast<std::map<std::string, std::any>>(headers.at(authKey));

            std::string userKey = "user";
            if (auth.find(userKey) == auth.end()) {
                return std::nullopt;
            }
            auto userMap = std::any_cast<std::map<std::string, std::any>>(auth.at(userKey));

            std::string jwtKey = "jwt";
            if (auth.find(jwtKey) == auth.end()) {
                return std::nullopt;
            }
            auto jwt = std::any_cast<std::string>(auth.at(jwtKey));

            // Check if jwt starts with the user's name
            std::string userName;
            if (userMap.find("name") != userMap.end()) {
                userName = std::any_cast<std::string>(userMap.at("name"));
            } else {
                return std::nullopt;
            }

            if (jwt.substr(0, userName.size()) != userName) {
                return std::nullopt;
            }

            // Parse the jwt date part
            std::string jwtDateStr = jwt.substr(userName.size());
            auto jwtDate = parse_date(jwtDateStr);
            if (!jwtDate) {
                return std::nullopt;
            }

            // Get current date
            auto now = date::floor<date::days>(date::system_clock::now());
            auto threeDaysAgo = now - date::days(3);

            if (threeDaysAgo > *jwtDate) {
                return std::nullopt;
            }

            return auth;
        } catch (...) {
            return std::nullopt;
        }
    }

    void setCurrentUserInfoAndLog(const std::map<std::string, std::any>& user) {
        try {
            std::string addressKey = "address";
            if (user.find(addressKey) == user.end()) {
                return;
            }
            std::string address = std::any_cast<std::string>(user.at(addressKey));
            std::string name = std::any_cast<std::string>(user.at("name"));
            auto now = date::floor<date::days>(date::system_clock::now());
            std::ostringstream oss;
            oss << name << address << now;
            std::cout << oss.str() << std::endl;
        } catch (...) {
            // If any error occurs, just return without logging.
            return;
        }
    }
};