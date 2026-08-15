#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <utility>
#include <variant>
#include <optional>
#include <stdexcept>
#include <cctype>
#include <cmath>
#include <iomanip>
#include <charconv>

class Json {
public:
    using Object = std::vector<std::pair<std::string, Json>>;
    using Array = std::vector<Json>;

    std::variant<std::nullptr_t, bool, long long, double, std::string, Array, Object> value;

    Json() : value(nullptr) {}
    Json(std::nullptr_t) : value(nullptr) {}
    Json(bool b) : value(b) {}
    Json(long long n) : value(n) {}
    Json(double d) : value(d) {}
    Json(const std::string& s) : value(s) {}
    Json(const char* s) : value(std::string(s)) {}
    Json(const Array& a) : value(a) {}
    Json(const Object& o) : value(o) {}

    bool isNull() const { return std::holds_alternative<std::nullptr_t>(value); }
    bool isBool() const { return std::holds_alternative<bool>(value); }
    bool isNumber() const { return std::holds_alternative<long long>(value) || std::holds_alternative<double>(value); }
    bool isInteger() const { return std::holds_alternative<long long>(value); }
    bool isString() const { return std::holds_alternative<std::string>(value); }
    bool isArray() const { return std::holds_alternative<Array>(value); }
    bool isObject() const { return std::holds_alternative<Object>(value); }

    bool asBool() const { return std::get<bool>(value); }
    long long asInteger() const { return std::get<long long>(value); }
    double asDouble() const { return std::get<double>(value); }
    const std::string& asString() const { return std::get<std::string>(value); }
    const Array& asArray() const { return std::get<Array>(value); }
    Array& asArray() { return std::get<Array>(value); }
    const Object& asObject() const { return std::get<Object>(value); }
    Object& asObject() { return std::get<Object>(value); }
};

static std::string json_escape(const std::string& s) {
    std::ostringstream oss;
    oss << '"';
    size_t i = 0;
    while (i < s.size()) {
        unsigned char c = static_cast<unsigned char>(s[i]);
        if (c == '"') { oss << "\\\""; i++; }
        else if (c == '\\') { oss << "\\\\"; i++; }
        else if (c == '\b') { oss << "\\b"; i++; }
        else if (c == '\f') { oss << "\\f"; i++; }
        else if (c == '\n') { oss << "\\n"; i++; }
        else if (c == '\r') { oss << "\\r"; i++; }
        else if (c == '\t') { oss << "\\t"; i++; }
        else if (c < 0x20) {
            oss << "\\u" << std::hex << std::setw(4) << std::setfill('0') << static_cast<int>(c);
            i++;
        } else if (c < 0x80) {
            oss << c;
            i++;
        } else {
            unsigned int cp = 0;
            int extra = 0;
            if ((c & 0xE0) == 0xC0) { cp = c & 0x1F; extra = 1; }
            else if ((c & 0xF0) == 0xE0) { cp = c & 0x0F; extra = 2; }
            else if ((c & 0xF8) == 0xF0) { cp = c & 0x07; extra = 3; }
            else { oss << c; i++; continue; }

            if (i + extra >= s.size()) { oss << c; i++; continue; }
            bool ok = true;
            for (int j = 1; j <= extra; j++) {
                unsigned char cc = static_cast<unsigned char>(s[i + j]);
                if ((cc & 0xC0) != 0x80) { ok = false; break; }
                cp = (cp << 6) | (cc & 0x3F);
            }
            if (!ok) { oss << c; i++; continue; }
            i += extra + 1;

            if (cp < 0x10000) {
                oss << "\\u" << std::hex << std::setw(4) << std::setfill('0') << cp;
            } else {
                cp -= 0x10000;
                unsigned int high = 0xD800 + (cp >> 10);
                unsigned int low = 0xDC00 + (cp & 0x3FF);
                oss << "\\u" << std::hex << std::setw(4) << std::setfill('0') << high;
                oss << "\\u" << std::hex << std::setw(4) << std::setfill('0') << low;
            }
        }
    }
    oss << '"';
    return oss.str();
}

static std::string double_to_string(double d) {
    if (std::isnan(d)) return "NaN";
    if (std::isinf(d)) return d > 0 ? "Infinity" : "-Infinity";

    char buf[128];
    auto res = std::to_chars(buf, buf + sizeof(buf), d);
    std::string s(buf, res.ptr);
    if (s.find('.') == std::string::npos &&
        s.find('e') == std::string::npos &&
        s.find('E') == std::string::npos) {
        s += ".0";
    }
    return s;
}

static std::string json_dump(const Json& j) {
    if (j.isNull()) return "null";
    if (j.isBool()) return j.asBool() ? "true" : "false";
    if (j.isInteger()) return std::to_string(j.asInteger());
    if (j.isNumber()) return double_to_string(j.asDouble());
    if (j.isString()) return json_escape(j.asString());

    if (j.isArray()) {
        std::string result = "[";
        const auto& arr = j.asArray();
        for (size_t i = 0; i < arr.size(); i++) {
            if (i > 0) result += ", ";
            result += json_dump(arr[i]);
        }
        result += "]";
        return result;
    }

    if (j.isObject()) {
        std::string result = "{";
        const auto& obj = j.asObject();
        for (size_t i = 0; i < obj.size(); i++) {
            if (i > 0) result += ", ";
            result += json_escape(obj[i].first);
            result += ": ";
            result += json_dump(obj[i].second);
        }
        result += "}";
        return result;
    }

    return "null";
}

class JsonParser {
public:
    JsonParser(const std::string& text) : s(text), pos(0) {}

    Json parse() {
        Json j = parseValue();
        skipWhitespace();
        if (pos != s.size()) throw std::runtime_error("Trailing characters");
        return j;
    }

private:
    const std::string& s;
    size_t pos;

    void skipWhitespace() {
        while (pos < s.size() && std::isspace(static_cast<unsigned char>(s[pos]))) pos++;
    }

    char peek() {
        if (pos >= s.size()) throw std::runtime_error("Unexpected end");
        return s[pos];
    }

    char get() {
        if (pos >= s.size()) throw std::runtime_error("Unexpected end");
        return s[pos++];
    }

    Json parseValue() {
        skipWhitespace();
        char c = peek();
        if (c == '{') return parseObject();
        if (c == '[') return parseArray();
        if (c == '"') return Json(parseString());
        if (c == 't' || c == 'f') return parseBool();
        if (c == 'n') return parseNull();
        if (c == '-' || std::isdigit(static_cast<unsigned char>(c))) return parseNumber();
        throw std::runtime_error("Unexpected character");
    }

    Json parseObject() {
        get(); // '{'
        Json::Object obj;
        skipWhitespace();
        if (peek() == '}') { get(); return Json(obj); }
        while (true) {
            skipWhitespace();
            if (peek() != '"') throw std::runtime_error("Expected string key");
            std::string key = parseString();
            skipWhitespace();
            if (get() != ':') throw std::runtime_error("Expected ':'");
            Json val = parseValue();

            bool found = false;
            for (auto& kv : obj) {
                if (kv.first == key) { kv.second = val; found = true; break; }
            }
            if (!found) obj.emplace_back(key, val);

            skipWhitespace();
            char c = get();
            if (c == ',') continue;
            if (c == '}') break;
            throw std::runtime_error("Expected ',' or '}'");
        }
        return Json(obj);
    }

    Json parseArray() {
        get(); // '['
        Json::Array arr;
        skipWhitespace();
        if (peek() == ']') { get(); return Json(arr); }
        while (true) {
            arr.push_back(parseValue());
            skipWhitespace();
            char c = get();
            if (c == ',') continue;
            if (c == ']') break;
            throw std::runtime_error("Expected ',' or ']'");
        }
        return Json(arr);
    }

    std::string parseString() {
        get(); // '"'
        std::string result;
        while (true) {
            char c = get();
            if (c == '"') break;
            if (c == '\\') {
                char e = get();
                switch (e) {
                    case '"': result += '"'; break;
                    case '\\': result += '\\'; break;
                    case '/': result += '/'; break;
                    case 'b': result += '\b'; break;
                    case 'f': result += '\f'; break;
                    case 'n': result += '\n'; break;
                    case 'r': result += '\r'; break;
                    case 't': result += '\t'; break;
                    case 'u': {
                        if (pos + 4 > s.size()) throw std::runtime_error("Invalid unicode escape");
                        unsigned int cp = 0;
                        for (int i = 0; i < 4; i++) {
                            char h = s[pos++];
                            cp <<= 4;
                            if (h >= '0' && h <= '9') cp |= (h - '0');
                            else if (h >= 'a' && h <= 'f') cp |= (h - 'a' + 10);
                            else if (h >= 'A' && h <= 'F') cp |= (h - 'A' + 10);
                            else throw std::runtime_error("Invalid hex digit");
                        }
                        if (cp >= 0xD800 && cp <= 0xDBFF) {
                            if (pos + 2 <= s.size() && s[pos] == '\\' && s[pos + 1] == 'u') {
                                pos += 2;
                                unsigned int cp2 = 0;
                                for (int i = 0; i < 4; i++) {
                                    char h = s[pos++];
                                    cp2 <<= 4;
                                    if (h >= '0' && h <= '9') cp2 |= (h - '0');
                                    else if (h >= 'a' && h <= 'f') cp2 |= (h - 'a' + 10);
                                    else if (h >= 'A' && h <= 'F') cp2 |= (h - 'A' + 10);
                                    else throw std::runtime_error("Invalid hex digit");
                                }
                                if (cp2 >= 0xDC00 && cp2 <= 0xDFFF) {
                                    cp = 0x10000 + ((cp - 0xD800) << 10) + (cp2 - 0xDC00);
                                } else {
                                    throw std::runtime_error("Invalid low surrogate");
                                }
                            } else {
                                throw std::runtime_error("Missing low surrogate");
                            }
                        }
                        if (cp < 0x80) {
                            result += static_cast<char>(cp);
                        } else if (cp < 0x800) {
                            result += static_cast<char>(0xC0 | (cp >> 6));
                            result += static_cast<char>(0x80 | (cp & 0x3F));
                        } else if (cp < 0x10000) {
                            result += static_cast<char>(0xE0 | (cp >> 12));
                            result += static_cast<char>(0x80 | ((cp >> 6) & 0x3F));
                            result += static_cast<char>(0x80 | (cp & 0x3F));
                        } else {
                            result += static_cast<char>(0xF0 | (cp >> 18));
                            result += static_cast<char>(0x80 | ((cp >> 12) & 0x3F));
                            result += static_cast<char>(0x80 | ((cp >> 6) & 0x3F));
                            result += static_cast<char>(0x80 | (cp & 0x3F));
                        }
                        break;
                    }
                    default: throw std::runtime_error("Invalid escape");
                }
            } else {
                result += c;
            }
        }
        return result;
    }

    Json parseBool() {
        if (s.compare(pos, 4, "true") == 0) {
            pos += 4;
            return Json(true);
        } else if (s.compare(pos, 5, "false") == 0) {
            pos += 5;
            return Json(false);
        }
        throw std::runtime_error("Invalid literal");
    }

    Json parseNull() {
        if (s.compare(pos, 4, "null") == 0) {
            pos += 4;
            return Json(nullptr);
        }
        throw std::runtime_error("Invalid literal");
    }

    Json parseNumber() {
        size_t start = pos;
        if (peek() == '-') get();
        while (pos < s.size() && std::isdigit(static_cast<unsigned char>(s[pos]))) get();

        bool isDouble = false;
        if (pos < s.size() && s[pos] == '.') {
            isDouble = true;
            get();
            while (pos < s.size() && std::isdigit(static_cast<unsigned char>(s[pos]))) get();
        }
        if (pos < s.size() && (s[pos] == 'e' || s[pos] == 'E')) {
            isDouble = true;
            get();
            if (pos < s.size() && (s[pos] == '+' || s[pos] == '-')) get();
            while (pos < s.size() && std::isdigit(static_cast<unsigned char>(s[pos]))) get();
        }

        std::string numStr = s.substr(start, pos - start);
        try {
            if (!isDouble) {
                size_t idx;
                long long n = std::stoll(numStr, &idx);
                if (idx != numStr.size()) throw std::runtime_error("Invalid number");
                return Json(n);
            } else {
                size_t idx;
                double d = std::stod(numStr, &idx);
                if (idx != numStr.size()) throw std::runtime_error("Invalid number");
                return Json(d);
            }
        } catch (...) {
            throw std::runtime_error("Invalid number");
        }
    }
};

static std::string python_repr(const Json& j) {
    if (j.isNull()) return "None";
    if (j.isBool()) return j.asBool() ? "True" : "False";
    if (j.isInteger()) return std::to_string(j.asInteger());
    if (j.isNumber()) return double_to_string(j.asDouble());

    if (j.isString()) {
        std::string result = "'";
        for (char c : j.asString()) {
            if (c == '\\' || c == '\'') result += '\\';
            result += c;
        }
        result += "'";
        return result;
    }

    if (j.isArray()) {
        std::string result = "[";
        const auto& arr = j.asArray();
        for (size_t i = 0; i < arr.size(); i++) {
            if (i > 0) result += ", ";
            result += python_repr(arr[i]);
        }
        result += "]";
        return result;
    }

    if (j.isObject()) {
        std::string result = "{";
        const auto& obj = j.asObject();
        for (size_t i = 0; i < obj.size(); i++) {
            if (i > 0) result += ", ";
            result += python_repr(Json(obj[i].first));
            result += ": ";
            result += python_repr(obj[i].second);
        }
        result += "}";
        return result;
    }

    return "None";
}

static std::string python_str(const Json& j) {
    if (j.isString()) return j.asString();
    return python_repr(j);
}

class CookiesUtil {
public:
    std::string cookies_file;
    std::optional<Json> cookies;

    CookiesUtil(const std::string& cookies_file) : cookies_file(cookies_file), cookies(std::nullopt) {}

    void get_cookies(const Json& response) {
        if (!response.isObject()) throw std::runtime_error("Response must be an object");
        const auto& obj = response.asObject();
        for (const auto& kv : obj) {
            if (kv.first == "cookies") {
                cookies = kv.second;
                _save_cookies();
                return;
            }
        }
        throw std::out_of_range("cookies");
    }

    Json load_cookies() {
        std::ifstream file(cookies_file);
        if (!file.is_open()) {
            return Json(Json::Object{});
        }
        std::stringstream buffer;
        buffer << file.rdbuf();
        std::string text = buffer.str();
        if (text.empty()) {
            throw std::runtime_error("Empty JSON file");
        }
        JsonParser parser(text);
        return parser.parse();
    }

    bool _save_cookies() {
        try {
            std::ofstream file(cookies_file);
            if (!file.is_open()) return false;
            if (cookies.has_value()) {
                file << json_dump(*cookies);
            } else {
                file << "null";
            }
            return true;
        } catch (...) {
            return false;
        }
    }

    void set_cookies(Json& request) {
        if (!cookies.has_value()) throw std::logic_error("cookies is None");
        if (!cookies->isObject()) throw std::logic_error("cookies is not an object");

        std::string result;
        bool first = true;
        for (const auto& kv : cookies->asObject()) {
            if (!first) result += "; ";
            first = false;
            result += kv.first;
            result += "=";
            result += python_str(kv.second);
        }

        if (!request.isObject()) throw std::runtime_error("Request must be an object");
        auto& obj = request.asObject();
        for (auto& kv : obj) {
            if (kv.first == "cookies") {
                kv.second = Json(result);
                return;
            }
        }
        obj.emplace_back("cookies", Json(result));
    }
};