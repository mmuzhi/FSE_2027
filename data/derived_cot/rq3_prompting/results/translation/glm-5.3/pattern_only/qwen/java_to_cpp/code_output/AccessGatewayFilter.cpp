#include <any>
#include <cctype>
#include <ctime>
#include <iomanip>
#include <iostream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>

using Map = std::map<std::string, std::any>;

class AccessGatewayFilter {
public:
    AccessGatewayFilter() = default;

    bool filter(Map& request) {
        std::string& requestUri = std::any_cast<std::string&>(request.at("path"));

        // Java: (String) request.get("method") -- null cast succeeds, value unused.
        auto methodIt = request.find("method");
        if (methodIt != request.end() && methodIt->second.has_value()) {
            std::any_cast<std::string&>(methodIt->second);
        }

        if (isStartWith(requestUri)) {
            return true;
        }

        try {
            std::any token = getJwtUser(request);  // empty any == Java null
            Map& user = std::any_cast<Map&>(std::any_cast<Map&>(token).at("user"));
            if (std::any_cast<int>(user.at("level")) > 2) {
                setCurrentUserInfoAndLog(user);
                return true;
            }
        } catch (const std::exception&) {
            return false;
        }
        return false;
    }

    bool isStartWith(const std::string& requestUri) {
        static const std::string startWith[] = {"/api", "/login"};
        for (const std::string& s : startWith) {
            if (requestUri.rfind(s, 0) == 0) {
                return true;
            }
        }
        return false;
    }

    std::any getJwtUser(Map& request) {
        Map& token = std::any_cast<Map&>(
            std::any_cast<Map&>(request.at("headers")).at("Authorization"));
        Map& user = std::any_cast<Map&>(token.at("user"));
        std::string& jwt = std::any_cast<std::string&>(token.at("jwt"));

        std::string& name = std::any_cast<std::string&>(user.at("name"));
        if (jwt.rfind(name, 0) == 0) {  // startsWith
            std::string jwtStrDate = jwt.substr(name.size());
            long long jwtDay = parseEpochDay(jwtStrDate);  // throws like DateTimeParseException
            // LocalDate.now().minusDays(3).isAfter(jwtDate)
            if (todayEpochDay() - 3 > jwtDay) {
                return std::any();  // null token
            }
        }
        return token;
    }

    void setCurrentUserInfoAndLog(Map& user) {
        std::string& host = std::any_cast<std::string&>(user.at("address"));
        std::string message = std::any_cast<std::string&>(user.at("name")) + host + todayString();
        std::cout << message << "\n";
    }

private:
    static bool isLeap(int y) {
        return (y % 4 == 0 && y % 100 != 0) || (y % 400 == 0);
    }

    static int daysInMonth(int y, int m) {
        static const int dm[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
        if (m == 2 && isLeap(y)) return 29;
        return dm[m - 1];
    }

    // Howard Hinnant's civil-date algorithm: days since 1970-01-01.
    static long long daysFromCivil(int y, int m, int d) {
        y -= (m <= 2);
        const int era = (y >= 0 ? y : y - 399) / 400;
        const unsigned yoe = static_cast<unsigned>(y - era * 400);
        const unsigned doy = (153u * static_cast<unsigned>(m + (m > 2 ? -3 : 9)) + 2u) / 5u
                             + static_cast<unsigned>(d) - 1u;
        const unsigned doe = yoe * 365u + yoe / 4u - yoe / 100u + doy;
        return static_cast<long long>(era) * 146097LL + static_cast<long long>(doe) - 719468LL;
    }

    static long long todayEpochDay() {
        std::time_t t = std::time(nullptr);
        std::tm* lt = std::localtime(&t);
        return daysFromCivil(lt->tm_year + 1900, lt->tm_mon + 1, lt->tm_mday);
    }

    static std::string todayString() {
        std::time_t t = std::time(nullptr);
        std::tm* lt = std::localtime(&t);
        std::ostringstream oss;
        oss << std::put_time(lt, "%Y-%m-%d");  // ISO-8601, matches LocalDate.toString()
        return oss.str();
    }

    // Parses "yyyy-MM-dd"; throws on malformed/invalid dates (like LocalDate.parse).
    static long long parseEpochDay(const std::string& s) {
        if (s.size() != 10 || s[4] != '-' || s[7] != '-') {
            throw std::runtime_error("DateTimeParseException");
        }
        static const int digitPos[] = {0, 1, 2, 3, 5, 6, 8, 9};
        for (int i : digitPos) {
            if (!std::isdigit(static_cast<unsigned char>(s[i]))) {
                throw std::runtime_error("DateTimeParseException");
            }
        }
        int y = std::stoi(s.substr(0, 4));
        int m = std::stoi(s.substr(5, 2));
        int d = std::stoi(s.substr(8, 2));
        if (m < 1 || m > 12 || d < 1 || d > daysInMonth(y, m)) {
            throw std::runtime_error("DateTimeParseException");
        }
        return daysFromCivil(y, m, d);
    }
};