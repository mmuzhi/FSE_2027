// C++ translation of the Python AccessGatewayFilter module.
// Python dicts are modelled with a small variant Value type; missing keys /
// wrong types raise exceptions like KeyError/TypeError, which filter() catches
// with catch(...) exactly like the bare `except:`. filter() may return
// std::nullopt, which corresponds to the Python implicit `None` return.

#include <cctype>
#include <chrono>
#include <cstdio>
#include <ctime>
#include <map>
#include <optional>
#include <stdexcept>
#include <string>
#include <variant>
#include <vector>

namespace pylike {

struct Value;
using Dict = std::map<std::string, Value>;

struct Value {
    std::variant<std::monostate, std::string, long long, Dict> data;

    Value() = default;
    Value(const char* s) : data(std::string(s)) {}
    Value(std::string s) : data(std::move(s)) {}
    Value(int n) : data(static_cast<long long>(n)) {}
    Value(long long n) : data(n) {}
    Value(Dict d) : data(std::move(d)) {}

    bool is_str() const { return std::holds_alternative<std::string>(data); }
    bool is_int() const { return std::holds_alternative<long long>(data); }

    // d[key]: raises KeyError-like error when missing or not a dict
    const Value& at(const std::string& key) const {
        if (!std::holds_alternative<Dict>(data))
            throw std::runtime_error("TypeError: value is not subscriptable");
        const Dict& d = std::get<Dict>(data);
        auto it = d.find(key);
        if (it == d.end()) throw std::runtime_error("KeyError: '" + key + "'");
        return it->second;
    }

    const std::string& as_str() const {  // str operations require a str
        if (!is_str()) throw std::runtime_error("TypeError: value is not a str");
        return std::get<std::string>(data);
    }

    long long as_int() const {  // int comparison requires an int
        if (!is_int()) throw std::runtime_error("TypeError: value is not an int");
        return std::get<long long>(data);
    }
};

bool startswith(const std::string& s, const std::string& prefix) {
    return s.size() >= prefix.size() && s.compare(0, prefix.size(), prefix) == 0;
}

std::vector<std::string> split(const std::string& s, const std::string& sep) {  // str.split(sep)
    if (sep.empty()) throw std::runtime_error("ValueError: empty separator");
    std::vector<std::string> out;
    size_t start = 0;
    for (;;) {
        size_t pos = s.find(sep, start);
        if (pos == std::string::npos) { out.push_back(s.substr(start)); break; }
        out.push_back(s.substr(start, pos - start));
        start = pos + sep.size();
    }
    return out;
}

// Days since 1970-01-01 (Howard Hinnant's algorithm).
long long days_from_civil(long long y, int m, int d) {
    y -= m <= 2;
    const long long era = (y >= 0 ? y : y - 399) / 400;
    const int yoe = static_cast<int>(y - era * 400);
    const int doy = (153 * (m + (m > 2 ? -3 : 9)) + 2) / 5 + d - 1;
    const int doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
    return era * 146097 + doe - 719468;
}

// datetime.datetime.today(): naive local wall-clock seconds since epoch frame.
long long local_naive_seconds_now() {
    std::time_t t = std::time(nullptr);
    std::tm tmv{};
#ifdef _WIN32
    localtime_s(&tmv, &t);
#else
    localtime_r(&t, &tmv);
#endif
    return days_from_civil(tmv.tm_year + 1900LL, tmv.tm_mon + 1, tmv.tm_mday) * 86400
         + tmv.tm_hour * 3600 + tmv.tm_min * 60 + tmv.tm_sec;
}

struct Ymd { long long y; int m, d; };

// datetime.datetime.strptime(s, "%Y-%m-%d"): 4-digit year, 1-2 digit month/day,
// no trailing data, valid calendar date; otherwise ValueError.
Ymd strptime_ymd(const std::string& s) {
    auto value_error = [] {
        throw std::runtime_error("ValueError: time data does not match format '%Y-%m-%d'");
    };
    if (s.size() < 8) value_error();  // shortest valid string: "YYYY-M-D"

    size_t i = 0;
    long long y = 0;
    for (int k = 0; k < 4; ++k, ++i) {  // %Y: exactly four digits
        if (!std::isdigit(static_cast<unsigned char>(s[i]))) value_error();
        y = y * 10 + (s[i] - '0');
    }
    if (s[i++] != '-') value_error();

    auto read_field = [&](int& out) {  // %m / %d: one or two digits
        int v = 0, n = 0;
        while (n < 2 && i < s.size() && std::isdigit(static_cast<unsigned char>(s[i]))) {
            v = v * 10 + (s[i++] - '0');
            ++n;
        }
        if (n == 0) value_error();
        out = v;
    };

    int m = 0, d = 0;
    read_field(m);
    if (i >= s.size() || s[i++] != '-') value_error();
    read_field(d);
    if (i != s.size()) value_error();  // "unconverted data remains"

    if (m < 1 || m > 12) value_error();
    static const int mdays[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    int maxd = mdays[m - 1];
    if (m == 2 && ((y % 4 == 0 && y % 100 != 0) || y % 400 == 0)) maxd = 29;
    if (d < 1 || d > maxd) value_error();
    return {y, m, d};
}

// str(datetime.datetime.now()): "YYYY-MM-DD HH:MM:SS.ffffff", local time.
std::string datetime_now_str() {
    using namespace std::chrono;
    const auto now = system_clock::now();
    const std::time_t t = system_clock::to_time_t(now);
    const long long us = duration_cast<microseconds>(now.time_since_epoch()).count() % 1000000;
    std::tm tmv{};
#ifdef _WIN32
    localtime_s(&tmv, &t);
#else
    localtime_r(&t, &tmv);
#endif
    char buf[40];
    std::snprintf(buf, sizeof buf, "%04d-%02d-%02d %02d:%02d:%02d.%06lld",
                  tmv.tm_year + 1900, tmv.tm_mon + 1, tmv.tm_mday,
                  tmv.tm_hour, tmv.tm_min, tmv.tm_sec, us);
    return buf;
}

// logging.log(level, msg): with Python's default root-logger level
// (WARNING = 30), a level-1 message produces no output.
class Logger {
public:
    static Logger& instance() { static Logger l; return l; }
    void log(long long level, const std::string& msg) const {
        if (level >= threshold_) std::fprintf(stderr, "%s\n", msg.c_str());
    }

private:
    Logger() = default;
    long long threshold_ = 30;  // logging.WARNING
};

}  // namespace pylike

class AccessGatewayFilter {
public:
    AccessGatewayFilter() = default;

    // True / False, or std::nullopt for the Python implicit `None`
    // (valid token whose user level is <= 2).
    std::optional<bool> filter(const pylike::Value& request) {
        const std::string& request_uri = request.at("path").as_str();
        (void)request.at("method");  // method = request['method']

        if (is_start_with(request_uri)) {
            return true;
        }

        try {
            std::optional<pylike::Value> token = get_jwt_user(request);
            if (!token.has_value())  // token['user'] on None -> TypeError
                throw std::runtime_error("TypeError: 'NoneType' object is not subscriptable");
            const pylike::Value& user = token->at("user");
            if (user.at("level").as_int() > 2) {
                set_current_user_info_and_log(user);
                return true;
            }
        } catch (...) {  // bare `except:`
            return false;
        }
        return std::nullopt;
    }

    bool is_start_with(const std::string& request_uri) {
        static const std::vector<std::string> start_with = {"/api", "/login"};
        for (const std::string& s : start_with) {
            if (pylike::startswith(request_uri, s)) {
                return true;
            }
        }
        return false;
    }

    // The token, or std::nullopt for the Python `None` (jwt too old).
    std::optional<pylike::Value> get_jwt_user(const pylike::Value& request) {
        const pylike::Value& token = request.at("headers").at("Authorization");
        const pylike::Value& user = token.at("user");
        const std::string& name = user.at("name").as_str();
        const std::string& jwt = token.at("jwt").as_str();
        if (pylike::startswith(jwt, name)) {
            const std::string& jwt_str_date = pylike::split(jwt, name).at(1);
            const pylike::Ymd jd = pylike::strptime_ymd(jwt_str_date);
            const long long jwt_naive = pylike::days_from_civil(jd.y, jd.m, jd.d) * 86400;
            if (pylike::local_naive_seconds_now() - jwt_naive >= 3LL * 86400) {
                return std::nullopt;
            }
        }
        return token;  // returns the token, as in Python
    }

    void set_current_user_info_and_log(const pylike::Value& user) {
        const std::string& host = user.at("address").as_str();
        pylike::Logger::instance().log(
            1, user.at("name").as_str() + host + pylike::datetime_now_str());
    }
};