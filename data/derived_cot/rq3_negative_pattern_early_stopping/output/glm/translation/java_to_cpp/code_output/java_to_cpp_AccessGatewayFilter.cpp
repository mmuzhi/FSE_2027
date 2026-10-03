#include <iostream>
#include <string>
#include <map>
#include <any>
#include <chrono>
#include <iomanip>
#include <sstream>

class AccessGatewayFilter {
public:
    AccessGatewayFilter() {}

    bool filter(std::map<std::string, std::any>& request) {
        std::string requestUri = std::any_cast<std::string>(request.at("path"));
        std::string method = std::any_cast<std::string>(request.at("method"));

        if (isStartWith(requestUri)) {
            return true;
        }

        try {
            std::map<std::string, std::any> token = getJwtUser(request);
            std::map<std::string, std::any> user = std::any_cast<std::map<std::string, std::any>>(token.at("user"));
            if (std::any_cast<int>(user.at("level")) > 2) {
                setCurrentUserInfoAndLog(user);
                return true;
            }
        } catch (const std::exception& e) {
            return false;
        }
        return false;
    }

    bool isStartWith(const std::string& requestUri) {
        std::string startWith[] = {"/api", "/login"};
        for (const std::string& s : startWith) {
            if (requestUri.size() >= s.size() && requestUri.substr(0, s.size()) == s) {
                return true;
            }
        }
        return false;
    }

    std::map<std::string, std::any> getJwtUser(std::map<std::string, std::any>& request) {
        std::map<std::string, std::any> headers = std::any_cast<std::map<std::string, std::any>>(request.at("headers"));
        std::map<std::string, std::any> token = std::any_cast<std::map<std::string, std::any>>(headers.at("Authorization"));
        std::map<std::string, std::any> user = std::any_cast<std::map<std::string, std::any>>(token.at("user"));
        std::string jwt = std::any_cast<std::string>(token.at("jwt"));
        std::string name = std::any_cast<std::string>(user.at("name"));

        if (jwt.size() >= name.size() && jwt.substr(0, name.size()) == name) {
            std::string jwtStrDate = jwt.substr(name.size());
            std::tm tm = {};
            std::istringstream iss(jwtStrDate);
            iss >> std::get_time(&tm, "%Y-%m-%d");
            if (iss.fail()) {
                return {};
            }
            auto jwtDate = std::chrono::year_month_day{
                std::chrono::year{tm.tm_year + 1900},
                std::chrono::month{static_cast<unsigned>(tm.tm_mon + 1)},
                std::chrono::day{static_cast<unsigned>(tm.tm_mday)}
            };
            auto now = std::chrono::year_month_day{
                std::chrono::floor<std::chrono::days>(std::chrono::system_clock::now())
            };
            auto jwtDateSys = std::chrono::sys_days{jwtDate};
            auto nowMinus3 = std::chrono::sys_days{now} - std::chrono::days{3};
            if (nowMinus3 > jwtDateSys) {
                return {};
            }
        }
        return token;
    }

    void setCurrentUserInfoAndLog(std::map<std::string, std::any>& user) {
        std::string host = std::any_cast<std::string>(user.at("address"));
        std::string name = std::any_cast<std::string>(user.at("name"));
        auto now = std::chrono::year_month_day{
            std::chrono::floor<std::chrono::days>(std::chrono::system_clock::now())
        };
        std::cout << name << host << now << std::endl;
    }
};