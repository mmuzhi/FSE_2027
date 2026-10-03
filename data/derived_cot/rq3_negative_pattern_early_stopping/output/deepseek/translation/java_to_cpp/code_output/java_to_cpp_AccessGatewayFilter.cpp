#include <any>
#include <chrono>
#include <ctime>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

class AccessGatewayFilter {
public:
    using AnyMap = std::map<std::string, std::any>;

    bool filter(AnyMap& request) {
        std::string requestUri = std::any_cast<std::string>(request.at("path"));
        std::string method = std::any_cast<std::string>(request.at("method"));
        (void)method; // unused in original but kept for parity

        if (isStartWith(requestUri)) {
            return true;
        }

        try {
            std::any tokenAny = getJwtUser(request);
            // If tokenAny is empty, any_cast throws bad_any_cast
            AnyMap token = std::any_cast<AnyMap>(tokenAny);
            AnyMap user = std::any_cast<AnyMap>(token.at("user"));
            int level = std::any_cast<int>(user.at("level"));
            if (level > 2) {
                setCurrentUserInfoAndLog(user);
                return true;
            }
        } catch (const std::exception&) {
            return false;
        }
        return false;
    }

    bool isStartWith(const std::string& requestUri) {
        std::vector<std::string> startWith = {"/api", "/login"};
        for (const auto& s : startWith) {
            if (requestUri.rfind(s, 0) == 0) {
                return true;
            }
        }
        return false;
    }

    std::any getJwtUser(AnyMap& request) {
        AnyMap headers = std::any_cast<AnyMap>(request.at("headers"));
        AnyMap token = std::any_cast<AnyMap>(headers.at("Authorization"));
        AnyMap user = std::any_cast<AnyMap>(token.at("user"));
        std::string jwt = std::any_cast<std::string>(token.at("jwt"));
        std::string userName = std::any_cast<std::string>(user.at("name"));

        if (jwt.rfind(userName, 0) == 0) {
            std::string jwtStrDate = jwt.substr(userName.length());
            // Parse date "yyyy-MM-dd"
            if (jwtStrDate.length() != 10) {
                return std::any(); // mimic null
            }
            int year = std::stoi(jwtStrDate.substr(0, 4));
            int month = std::stoi(jwtStrDate.substr(5, 2));
            int day = std::stoi(jwtStrDate.substr(8, 2));

            // current date - 3 days
            auto now = std::chrono::system_clock::now();
            std::time_t t = std::chrono::system_clock::to_time_t(now);
            struct tm* local = std::localtime(&t);
            local->tm_mday -= 3;
            std::mktime(local);
            int curYear = local->tm_year + 1900;
            int curMonth = local->tm_mon + 1;
            int curDay = local->tm_mday;

            // days since epoch for comparison
            auto daysFromEpoch = [](int y, int m, int d) -> long long {
                if (m <= 2) { y--; m += 12; }
                return 365LL * y + y/4 - y/100 + y/400 + (153LL*m - 457)/5 + d - 306;
            };

            long long jwtDays = daysFromEpoch(year, month, day);
            long long curDays = daysFromEpoch(curYear, curMonth, curDay);

            if (curDays > jwtDays) { // 3 days before now is after jwtDate? Actually: now.minusDays(3).isAfter(jwtDate)
                // Equivalent to jwtDays < curDays
                return std::any(); // return null
            }
        }
        return std::any(token);
    }

    void setCurrentUserInfoAndLog(AnyMap& user) {
        std::string host = std::any_cast<std::string>(user.at("address"));
        std::string name = std::any_cast<std::string>(user.at("name"));

        auto now = std::chrono::system_clock::now();
        std::time_t t = std::chrono::system_clock::to_time_t(now);
        struct tm* local = std::localtime(&t);
        char buf[11];
        std::strftime(buf, sizeof(buf), "%Y-%m-%d", local);
        std::string today(buf);

        std::cout << name << host << today << std::endl;
    }
};