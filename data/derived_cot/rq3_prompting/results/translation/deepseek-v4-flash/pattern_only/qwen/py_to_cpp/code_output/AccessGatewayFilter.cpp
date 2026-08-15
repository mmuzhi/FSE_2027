#include <string>
#include <map>
#include <stdexcept>
#include <typeinfo>
#include <optional>
#include <chrono>
#include <ctime>
#include <sstream>
#include <iomanip>
#include <vector>

class Value {
public:
    enum class Type { Null, String, Int, Dict };

    Value() : type_(Type::Null), int_(0) {}
    Value(const std::string& s) : type_(Type::String), str_(s), int_(0) {}
    Value(const char* s) : type_(Type::String), str_(s), int_(0) {}
    Value(int i) : type_(Type::Int), int_(i) {}
    Value(const std::map<std::string, Value>& d) : type_(Type::Dict), int_(0), dict_(d) {}

    const Value& at(const std::string& key) const {
        if (type_ != Type::Dict) throw std::out_of_range("Value is not a dict");
        return dict_.at(key);
    }

    const std::string& as_string() const {
        if (type_ != Type::String) throw std::bad_cast();
        return str_;
    }

    int as_int() const {
        if (type_ != Type::Int) throw std::bad_cast();
        return int_;
    }

    bool is_null() const { return type_ == Type::Null; }

private:
    Type type_;
    std::string str_;
    int int_;
    std::map<std::string, Value> dict_;
};

class AccessGatewayFilter {
public:
    AccessGatewayFilter() {}

    std::optional<bool> filter(const Value& request) const {
        const Value& path_val = request.at("path");
        (void)request.at("method"); // unused, but preserves KeyError if missing
        const std::string& request_uri = path_val.as_string();

        if (is_start_with(request_uri)) {
            return true;
        }

        try {
            Value token = get_jwt_user(request);
            Value user = token.at("user");
            if (user.at("level").as_int() > 2) {
                set_current_user_info_and_log(user);
                return true;
            }
            return std::nullopt; // Python returns None
        } catch (...) {
            return false;
        }
    }

    bool is_start_with(const std::string& request_uri) const {
        static const std::vector<std::string> start_with = {"/api", "/login"};
        for (const auto& s : start_with) {
            if (request_uri.compare(0, s.size(), s) == 0) {
                return true;
            }
        }
        return false;
    }

    Value get_jwt_user(const Value& request) const {
        const Value& headers = request.at("headers");
        const Value& token = headers.at("Authorization");
        const Value& user = token.at("user");
        const std::string& jwt = token.at("jwt").as_string();
        const std::string& name = user.at("name").as_string();

        if (jwt.compare(0, name.size(), name) == 0) {
            if (name.empty()) {
                throw std::runtime_error("empty separator");
            }
            std::string jwt_str_date = split_index_1(jwt, name);
            std::tm tm = {};
            std::istringstream ss(jwt_str_date);
            ss >> std::get_time(&tm, "%Y-%m-%d");
            if (ss.fail() || ss.peek() != std::char_traits<char>::eof()) {
                throw std::runtime_error("date parse error");
            }
            std::tm original = tm;
            tm.tm_isdst = -1;
            std::time_t time = std::mktime(&tm);
            if (time == -1) {
                throw std::runtime_error("date parse error");
            }
            if (tm.tm_year != original.tm_year || tm.tm_mon != original.tm_mon || tm.tm_mday != original.tm_mday) {
                throw std::runtime_error("date parse error");
            }
            auto jwt_time = std::chrono::system_clock::from_time_t(time);
            auto now = std::chrono::system_clock::now();
            if (now - jwt_time >= std::chrono::hours(72)) {
                return Value(); // None
            }
        }
        return token;
    }

    void set_current_user_info_and_log(const Value& user) const {
        std::string host = user.at("address").as_string();
        std::string name = user.at("name").as_string();
        // Python's logging.log(level=1) is below the default level and is intentionally omitted.
        (void)host;
        (void)name;
    }

private:
    static std::string split_index_1(const std::string& s, const std::string& sep) {
        size_t first = s.find(sep);
        if (first == std::string::npos) {
            throw std::out_of_range("index");
        }
        size_t second = s.find(sep, first + sep.size());
        if (second == std::string::npos) {
            return s.substr(first + sep.size());
        } else {
            return s.substr(first + sep.size(), second - (first + sep.size()));
        }
    }
};