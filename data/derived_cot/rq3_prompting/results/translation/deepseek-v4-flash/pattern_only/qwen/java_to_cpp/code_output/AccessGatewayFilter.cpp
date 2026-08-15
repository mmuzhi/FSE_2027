#include <map>
#include <string>
#include <any>
#include <vector>
#include <iostream>
#include <stdexcept>
#include <ctime>
#include <typeinfo>

using AnyMap = std::map<std::string, std::any>;

// ---------- Date helpers (mimic LocalDate) ----------
bool isLeapYear(int y) {
    return (y % 4 == 0 && y % 100 != 0) || y % 400 == 0;
}

int daysInMonth(int y, int m) {
    static int days[] = {31,28,31,30,31,30,31,31,30,31,30,31};
    if (m == 2 && isLeapYear(y)) return 29;
    return days[m - 1];
}

struct Date {
    int year;
    int month;
    int day;
};

Date parseDate(const std::string& s) {
    if (s.size() != 10 || s[4] != '-' || s[7] != '-') {
        throw std::runtime_error("Invalid date format");
    }
    int y = std::stoi(s.substr(0, 4));
    int m = std::stoi(s.substr(5, 2));
    int d = std::stoi(s.substr(8, 2));

    // Mimic Java's SMART resolver: adjust out-of-range values
    if (m < 1) m = 1;
    if (m > 12) m = 12;
    int dim = daysInMonth(y, m);
    if (d < 1) d = 1;
    if (d > dim) d = dim;

    return {y, m, d};
}

int daysFromCivil(int y, int m, int d) {
    y -= m <= 2;
    const int era = (y >= 0 ? y : y - 399) / 400;
    const unsigned yoe = static_cast<unsigned>(y - era * 400);
    const unsigned doy = (153 * (m + (m > 2 ? -3 : 9)) + 2) / 5 + d - 1;
    const unsigned doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
    return era * 146097 + static_cast<int>(doe) - 719468;
}

int todayDays() {
    std::time_t t = std::time(nullptr);
    std::tm* tm = std::localtime(&t);
    return daysFromCivil(tm->tm_year + 1900, tm->tm_mon + 1, tm->tm_mday);
}

std::string todayString() {
    std::time_t t = std::time(nullptr);
    std::tm* tm = std::localtime(&t);
    char buf[11];
    std::strftime(buf, sizeof(buf), "%Y-%m-%d", tm);
    return std::string(buf);
}

// ---------- Java-like String.valueOf for std::any ----------
std::string javaStringValue(const std::any& a);

std::string mapToString(const AnyMap& m) {
    std::string result = "{";
    bool first = true;
    for (const auto& [k, v] : m) {
        if (!first) result += ", ";
        first = false;
        result += k;
        result += "=";
        result += javaStringValue(v);
    }
    result += "}";
    return result;
}

std::string javaStringValue(const std::any& a) {
    if (!a.has_value()) return "null";
    const std::type_info& t = a.type();
    if (t == typeid(std::string)) return std::any_cast<std::string>(a);
    if (t == typeid(const char*)) return std::any_cast<const char*>(a);
    if (t == typeid(int)) return std::to_string(std::any_cast<int>(a));
    if (t == typeid(long)) return std::to_string(std::any_cast<long>(a));
    if (t == typeid(long long)) return std::to_string(std::any_cast<long long>(a));
    if (t == typeid(double)) return std::to_string(std::any_cast<double>(a));
    if (t == typeid(bool)) return std::any_cast<bool>(a) ? "true" : "false";
    if (t == typeid(AnyMap)) return mapToString(std::any_cast<const AnyMap&>(a));
    throw std::bad_any_cast();
}

// ---------- Helpers for Java cast semantics ----------
AnyMap& asMap(std::any& a) {
    return std::any_cast<AnyMap&>(a);
}

const std::string* getStringOrNullPtr(const AnyMap& m, const std::string& key) {
    auto it = m.find(key);
    if (it == m.end() || !it->second.has_value()) return nullptr;
    const std::string* p = std::any_cast<std::string>(&it->second);
    if (!p) throw std::bad_any_cast();
    return p;
}

std::string getStringOrNull(const AnyMap& m, const std::string& key) {
    auto it = m.find(key);
    if (it == m.end() || !it->second.has_value()) return "null";
    return std::any_cast<std::string>(it->second);
}

// ---------- Translated class ----------
class AccessGatewayFilter {
public:
    AccessGatewayFilter() = default;

    bool filter(AnyMap& request) {
        const std::string* requestUri = getStringOrNullPtr(request, "path");

        // Mimic `String method = (String) request.get("method");` without using the value.
        auto methodIt = request.find("method");
        if (methodIt != request.end() && methodIt->second.has_value()) {
            std::any_cast<std::string>(methodIt->second);
        }

        if (isStartWith(requestUri)) {
            return true;
        }

        try {
            AnyMap* token = getJwtUser(request);
            if (token == nullptr) {
                return false;
            }
            AnyMap& user = asMap(token->at("user"));
            if (std::any_cast<int>(user.at("level")) > 2) {
                setCurrentUserInfoAndLog(user);
                return true;
            }
        } catch (...) {
            return false;
        }
        return false;
    }

    bool isStartWith(const std::string* requestUri) {
        if (!requestUri) {
            throw std::runtime_error("NullPointerException");
        }
        std::vector<std::string> startWith = {"/api", "/login"};
        for (const auto& s : startWith) {
            if (requestUri->rfind(s, 0) == 0) {
                return true;
            }
        }
        return false;
    }

    AnyMap* getJwtUser(AnyMap& request) {
        AnyMap& headers = asMap(request.at("headers"));
        AnyMap& token = asMap(headers.at("Authorization"));
        AnyMap& user = asMap(token.at("user"));
        std::string jwt = std::any_cast<std::string>(token.at("jwt"));
        std::string name = std::any_cast<std::string>(user.at("name"));

        if (jwt.rfind(name, 0) == 0) {
            std::string jwtStrDate = jwt.substr(name.length());
            Date d = parseDate(jwtStrDate);
            int jwtDays = daysFromCivil(d.year, d.month, d.day);
            int todayMinus3 = todayDays() - 3;
            if (todayMinus3 > jwtDays) {
                return nullptr;
            }
        }
        return &token;
    }

    void setCurrentUserInfoAndLog(AnyMap& user) {
        std::string host = getStringOrNull(user, "address");
        std::string name;
        auto nameIt = user.find("name");
        if (nameIt == user.end()) {
            name = "null";
        } else {
            name = javaStringValue(nameIt->second);
        }
        std::cout << name + host + todayString() << std::endl;
    }
};