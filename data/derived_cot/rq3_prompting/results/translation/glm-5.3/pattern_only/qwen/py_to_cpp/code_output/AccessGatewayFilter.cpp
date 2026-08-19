// This class is a filter used for accessing gateway filtering, primarily for
// authentication and access log recording.
#include <chrono>
#include <cstddef>
#include <cstdio>
#include <ctime>
#include <optional>
#include <stdexcept>
#include <string>

namespace {

// Emulates Python KeyError (missing dict entry).
struct KeyError : std::runtime_error {
    explicit KeyError(const std::string& key)
        : std::runtime_error("KeyError: '" + key + "'") {}
};

// Emulates Python ValueError (bad strptime input, empty separator, ...).
struct ValueError : std::runtime_error {
    explicit ValueError(const std::string& what) : std::runtime_error(what) {}
};

// Emulates Python TypeError (e.g. subscripting None).
struct TypeError : std::runtime_error {
    explicit TypeError(const std::string& what) : std::runtime_error(what) {}
};

// Emulates logging.log(level=1, msg=...): with default configuration the root
// logger's effective level is WARNING (30), so a level-1 record is discarded
// and nothing is emitted.
void log_record(int level, const std::string& msg) {
    if (level >= 30) {
        std::fputs((msg + "\n").c_str(), stderr);
    }
}

struct Ymd {
    long long y;
    unsigned m;
    unsigned d;
};

bool is_leap(long long y) { return y % 4 == 0 && (y % 100 != 0 || y % 400 == 0); }

unsigned days_in_month(long long y, unsigned m) {
    static const unsigned t[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    if (m == 2 && is_leap(y)) return 29;
    return t[m - 1];
}

// Days since 1970-01-01 for a civil date (Howard Hinnant's algorithm); lets us
// subtract naive datetimes exactly the way Python's datetime does.
long long days_from_civil(long long y, unsigned m, unsigned d) {
    y -= m <= 2;
    const long long era = (y >= 0 ? y : y - 399) / 400;
    const unsigned yoe = static_cast<unsigned>(y - era * 400);
    const unsigned doy = (153u * (m + (m > 2 ? -3u : 9u)) + 2u) / 5u + d - 1u;
    const unsigned doe = yoe * 365u + yoe / 4u - yoe / 100u + doy;
    return era * 146097 + static_cast<long long>(doe) - 719468;
}

// Emulates datetime.datetime.strptime(s, "%Y-%m-%d"): exactly four digits for
// the year, one or two digits for month/day, literal '-', the whole string
// must be consumed, and the resulting date must be valid.
Ymd parse_ymd(const std::string& s) {
    auto fail = [&s] {
        throw ValueError("time data '" + s + "' does not match format '%Y-%m-%d'");
    };
    auto digit = [&](std::size_t i) -> int {
        if (i >= s.size() || s[i] < '0' || s[i] > '9') return -1;
        return s[i] - '0';
    };
    if (s.size() < 8) fail();  // shortest valid form is "YYYY-M-D"
    int y = 0;
    for (int k = 0; k < 4; ++k) {
        int dg = digit(static_cast<std::size_t>(k));
        if (dg < 0) fail();
        y = y * 10 + dg;
    }
    if (s[4] != '-') fail();
    int m = digit(5);
    if (m < 0) fail();
    std::size_t i = 6;
    int m2 = digit(i);
    if (m2 >= 0) { m = m * 10 + m2; ++i; }
    if (i >= s.size() || s[i] != '-') fail();
    ++i;
    int d = digit(i);
    if (d < 0) fail();
    ++i;
    int d2 = digit(i);
    if (d2 >= 0) { d = d * 10 + d2; ++i; }
    if (i != s.size()) fail();  // "unconverted data remains"
    if (y < 1 || m < 1 || m > 12 || d < 1 ||
        d > static_cast<int>(days_in_month(y, static_cast<unsigned>(m)))) {
        fail();
    }
    return Ymd{y, static_cast<unsigned>(m), static_cast<unsigned>(d)};
}

// Local wall-clock seconds of "now" as a naive datetime (Python: datetime.today()).
long long naive_now_seconds() {
    std::time_t tt = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
    std::tm lt = *std::localtime(&tt);
    long long days = days_from_civil(lt.tm_year + 1900LL,
                                     static_cast<unsigned>(lt.tm_mon + 1),
                                     static_cast<unsigned>(lt.tm_mday));
    return days * 86400LL + lt.tm_hour * 3600 + lt.tm_min * 60 + lt.tm_sec;
}

// Emulates str(datetime.datetime.now()): "YYYY-MM-DD HH:MM:SS" plus ".ffffff"
// when the microsecond component is non-zero.
std::string format_now() {
    auto now = std::chrono::system_clock::now();
    std::time_t tt = std::chrono::system_clock::to_time_t(now);
    std::tm lt = *std::localtime(&tt);
    char buf[32];
    std::snprintf(buf, sizeof(buf), "%04d-%02d-%02d %02d:%02d:%02d",
                  lt.tm_year + 1900, lt.tm_mon + 1, lt.tm_mday,
                  lt.tm_hour, lt.tm_min, lt.tm_sec);
    std::string s(buf);
    long long us = std::chrono::duration_cast<std::chrono::microseconds>(
                       now.time_since_epoch()).count() % 1000000LL;
    if (us != 0) {
        char ubuf[9];
        std::snprintf(ubuf, sizeof(ubuf), ".%06lld", us);
        s += ubuf;
    }
    return s;
}

}  // namespace

class AccessGatewayFilter {
public:
    // Dict-shaped payload; each field is optional so that a missing key can
    // raise KeyError exactly where Python would.
    struct User {
        std::optional<std::string> name;
        std::optional<int> level;
        std::optional<std::string> address;
    };
    struct Token {
        std::optional<User> user;
        std::optional<std::string> jwt;
    };
    struct Headers {
        std::optional<Token> authorization;  // key: "Authorization"
    };
    struct Request {
        std::optional<std::string> path;
        std::optional<std::string> method;
        std::optional<Headers> headers;
    };

    AccessGatewayFilter() = default;

    // Filter the incoming request based on certain rules and conditions.
    // Returns true if the request is allowed, false otherwise (Python's
    // implicit None return is mapped to false).
    bool filter(const Request& request) {
        if (!request.path) throw KeyError("path");
        if (!request.method) throw KeyError("method");
        const std::string& request_uri = *request.path;
        [[maybe_unused]] const std::string& method = *request.method;

        if (is_start_with(request_uri)) {
            return true;
        }

        try {
            std::optional<Token> token = get_jwt_user(request);
            if (!token) throw TypeError("'NoneType' object is not subscriptable");
            if (!token->user) throw KeyError("user");
            const User& user = *token->user;
            if (!user.level) throw KeyError("level");
            if (*user.level > 2) {
                set_current_user_info_and_log(user);
                return true;
            }
        } catch (...) {
            return false;
        }
        return false;  // Python falls through and implicitly returns None
    }

    // Check if the request URI starts with "/api" or "/login".
    bool is_start_with(const std::string& request_uri) {
        static const char* const start_with[] = {"/api", "/login"};
        for (const char* s : start_with) {
            if (request_uri.rfind(s, 0) == 0) {  // str.startswith
                return true;
            }
        }
        return false;
    }

    // Get the user information from the JWT token in the request.
    // Returns the token if valid, std::nullopt if the JWT has expired.
    std::optional<Token> get_jwt_user(const Request& request) {
        if (!request.headers) throw KeyError("headers");
        if (!request.headers->authorization) throw KeyError("Authorization");
        const Token& token = *request.headers->authorization;
        if (!token.user) throw KeyError("user");
        if (!token.jwt) throw KeyError("jwt");
        const User& user = *token.user;
        if (!user.name) throw KeyError("name");
        const std::string& jwt = *token.jwt;
        const std::string& name = *user.name;

        if (jwt.rfind(name, 0) == 0) {  // jwt.startswith(name)
            if (name.empty()) throw ValueError("empty separator");
            // jwt.split(name)[1]: the text after the first occurrence
            std::size_t first = jwt.find(name);
            std::string jwt_str_date = jwt.substr(first + name.size());
            Ymd jd = parse_ymd(jwt_str_date);  // throws ValueError on mismatch
            long long now_secs = naive_now_seconds();
            long long jwt_secs =
                days_from_civil(jd.y, jd.m, jd.d) * 86400LL;  // midnight
            if (now_secs - jwt_secs >= 3LL * 86400LL) {  // >= timedelta(days=3)
                return std::nullopt;
            }
        }
        return token;
    }

    // Set the current user information and log the access.
    void set_current_user_info_and_log(const User& user) {
        if (!user.address) throw KeyError("address");
        if (!user.name) throw KeyError("name");
        const std::string& name = *user.name;
        const std::string& host = *user.address;
        log_record(1, name + host + format_now());
    }
};