#include <any>
#include <cstddef>
#include <cstdio>
#include <ctime>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>

namespace org {
namespace example {

using AnyMap = std::map<std::string, std::any>;

class AccessGatewayFilter {
public:
    AccessGatewayFilter() = default;

    bool filter(AnyMap& request) {
        std::string requestUri = std::any_cast<const std::string&>(request.at("path"));
        std::string method;
        std::map<std::string, std::any>::iterator itM = request.find("method");
        if (itM != request.end() && itM->second.has_value()) {
            method = std::any_cast<const std::string&>(itM->second);
        }
        (void)method; // unused, as in the Java source

        if (isStartWith(requestUri)) {
            return true;
        }

        try {
            std::any token = getJwtUser(request);
            AnyMap& tokenMap = std::any_cast<AnyMap&>(token);
            AnyMap& user = std::any_cast<AnyMap&>(tokenMap.at("user"));
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
        const std::string startWith[] = {"/api", "/login"};
        for (const std::string& s : startWith) {
            if (requestUri.rfind(s, 0) == 0) { // startsWith
                return true;
            }
        }
        return false;
    }

    std::any getJwtUser(AnyMap& request) {
        AnyMap& headers = std::any_cast<AnyMap&>(request.at("headers"));
        AnyMap& token = std::any_cast<AnyMap&>(headers.at("Authorization"));
        AnyMap& user = std::any_cast<AnyMap&>(token.at("user"));
        std::string jwt = std::any_cast<const std::string&>(token.at("jwt"));

        std::string name = std::any_cast<const std::string&>(user.at("name"));
        if (jwt.rfind(name, 0) == 0) { // jwt.startsWith(name)
            std::string jwtStrDate = jwt.substr(name.size());
            long jwtDay = parseDate(jwtStrDate); // yyyy-MM-dd, strict
            // LocalDate.now().minusDays(3).isAfter(jwtDate)
            if (todaySerial() - 3 > jwtDay) {
                return std::any(); // null token
            }
        }
        return token;
    }

    void setCurrentUserInfoAndLog(AnyMap& user) {
        std::string host = std::any_cast<const std::string&>(user.at("address"));
        std::string message = std::any_cast<const std::string&>(user.at("name")) + host + todayString();
        std::cout << message << std::endl;
    }

private:
    static bool allDigits(const std::string& s, std::size_t pos, std::size_t len) {
        for (std::size_t i = pos; i < pos + len; ++i) {
            if (s[i] < '0' || s[i] > '9') return false;
        }
        return true;
    }

    // Strict "yyyy-MM-dd" parse, mirroring DateTimeFormatter.ofPattern("yyyy-MM-dd")
    static long parseDate(const std::string& s) {
        if (s.size() != 10 || s[4] != '-' || s[7] != '-' ||
            !allDigits(s, 0, 4) || !allDigits(s, 5, 2) || !allDigits(s, 8, 2)) {
            throw std::runtime_error("Text '" + s + "' could not be parsed");
        }
        long y = std::stol(s.substr(0, 4));
        long m = std::stol(s.substr(5, 2));
        long d = std::stol(s.substr(8, 2));
        if (m < 1 || m > 12 || d < 1 || d > 31) {
            throw std::runtime_error("Text '" + s + "' could not be parsed");
        }
        return daysFromCivil(y, m, d);
    }

    static long todaySerial() {
        std::time_t t = std::time(nullptr);
        std::tm lt = *std::localtime(&t); // LocalDate.now() is the local date
        return daysFromCivil(lt.tm_year + 1900, lt.tm_mon + 1, lt.tm_mday);
    }

    static std::string todayString() { // LocalDate.toString() -> "yyyy-MM-dd"
        std::time_t t = std::time(nullptr);
        std::tm lt = *std::localtime(&t);
        char buf[16];
        std::snprintf(buf, sizeof(buf), "%04d-%02d-%02d",
                      lt.tm_year + 1900, lt.tm_mon + 1, lt.tm_mday);
        return std::string(buf);
    }

    // Days since civil epoch (proleptic Gregorian, same calendar as java.time.LocalDate)
    static long daysFromCivil(long y, long m, long d) {
        y -= m <= 2;
        const long era = (y >= 0 ? y : y - 399) / 400;
        const unsigned long yoe = static_cast<unsigned long>(y - era * 400);
        const unsigned long doy = (153 * (m + (m > 2 ? -3 : 9)) + 2) / 5 + d - 1;
        const unsigned long doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
        return era * 146097 + static_cast<long>(doe) - 719468;
    }
};

} // namespace example
} // namespace org