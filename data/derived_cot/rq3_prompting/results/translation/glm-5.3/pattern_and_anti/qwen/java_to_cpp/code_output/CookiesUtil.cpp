#include <cstdio>
#include <fstream>
#include <map>
#include <optional>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>

class CookiesUtil {
private:
    struct ParseException : std::runtime_error { using std::runtime_error::runtime_error; };
    struct ClassCastException : std::runtime_error { using std::runtime_error::runtime_error; };

    std::string cookiesFile;
    std::optional<std::map<std::string, std::string>> cookies;

    static std::string jsonEscape(const std::string& s) {
        std::string out;
        for (char c : s) {
            switch (c) {
                case '"': out += "\\\""; break;
                case '\\': out += "\\\\"; break;
                case '\b': out += "\\b"; break;
                case '\f': out += "\\f"; break;
                case '\n': out += "\\n"; break;
                case '\r': out += "\\r"; break;
                case '\t': out += "\\t"; break;
                default:
                    if (static_cast<unsigned char>(c) < 0x20) {
                        char buf[8];
                        std::snprintf(buf, sizeof(buf), "\\u%04x", static_cast<unsigned char>(c));
                        out += buf;
                    } else {
                        out += c;
                    }
            }
        }
        return out;
    }

    static void skipWs(const std::string& text, size_t& pos) {
        while (pos < text.size() &&
               (text[pos] == ' ' || text[pos] == '\t' || text[pos] == '\n' || text[pos] == '\r'))
            ++pos;
    }

    static std::string parseString(const std::string& text, size_t& pos) {
        ++pos; // skip opening quote
        std::string out;
        while (pos < text.size()) {
            char c = text[pos++];
            if (c == '"') return out;
            if (c == '\\') {
                if (pos >= text.size()) throw ParseException("Unterminated escape");
                char e = text[pos++];
                switch (e) {
                    case '"': out += '"'; break;
                    case '\\': out += '\\'; break;
                    case '/': out += '/'; break;
                    case 'b': out += '\b'; break;
                    case 'f': out += '\f'; break;
                    case 'n': out += '\n'; break;
                    case 'r': out += '\r'; break;
                    case 't': out += '\t'; break;
                    case 'u': {
                        if (pos + 4 > text.size()) throw ParseException("Bad \\u escape");
                        unsigned code = 0;
                        for (int i = 0; i < 4; ++i) {
                            char h = text[pos++];
                            code <<= 4;
                            if (h >= '0' && h <= '9') code |= static_cast<unsigned>(h - '0');
                            else if (h >= 'a' && h <= 'f') code |= static_cast<unsigned>(h - 'a' + 10);
                            else if (h >= 'A' && h <= 'F') code |= static_cast<unsigned>(h - 'A' + 10);
                            else throw ParseException("Bad hex digit");
                        }
                        if (code < 0x80) {
                            out += static_cast<char>(code);
                        } else if (code < 0x800) {
                            out += static_cast<char>(0xC0 | (code >> 6));
                            out += static_cast<char>(0x80 | (code & 0x3F));
                        } else {
                            out += static_cast<char>(0xE0 | (code >> 12));
                            out += static_cast<char>(0x80 | ((code >> 6) & 0x3F));
                            out += static_cast<char>(0x80 | (code & 0x3F));
                        }
                        break;
                    }
                    default: throw ParseException("Bad escape character");
                }
            } else {
                out += c;
            }
        }
        throw ParseException("Unterminated string");
    }

    static std::map<std::string, std::string> parseObject(const std::string& text, size_t& pos) {
        skipWs(text, pos);
        if (pos >= text.size() || text[pos] != '{') throw ParseException("Expected '{'");
        ++pos;
        std::map<std::string, std::string> result;
        skipWs(text, pos);
        if (pos < text.size() && text[pos] == '}') { ++pos; return result; }
        while (true) {
            skipWs(text, pos);
            if (pos >= text.size() || text[pos] != '"') throw ParseException("Expected string key");
            std::string key = parseString(text, pos);
            skipWs(text, pos);
            if (pos >= text.size() || text[pos] != ':') throw ParseException("Expected ':'");
            ++pos;
            skipWs(text, pos);
            // Java: (String) value cast throws ClassCastException for non-string values (not caught)
            if (pos >= text.size() || text[pos] != '"')
                throw ClassCastException("value is not a String");
            std::string value = parseString(text, pos);
            result[key] = value;
            skipWs(text, pos);
            if (pos >= text.size()) throw ParseException("Unterminated object");
            if (text[pos] == ',') { ++pos; continue; }
            if (text[pos] == '}') { ++pos; return result; }
            throw ParseException("Expected ',' or '}'");
        }
    }

public:
    explicit CookiesUtil(std::string cookiesFile_)
        : cookiesFile(std::move(cookiesFile_)), cookies(std::nullopt) {}

    void getCookies(const std::map<std::string, std::map<std::string, std::string>>& response) {
        auto it = response.find("cookies");
        if (it != response.end())
            cookies = it->second;
        else
            cookies = std::nullopt;
        _saveCookies();
    }

    std::map<std::string, std::string> loadCookies() {
        std::ifstream reader(cookiesFile);
        if (!reader.is_open()) return {}; // IOException (FileNotFoundException) -> empty map
        try {
            std::stringstream ss;
            ss << reader.rdbuf();
            size_t pos = 0;
            return parseObject(ss.str(), pos);
        } catch (const ParseException&) {
            return {}; // ParseException -> empty map
        }
    }

    bool _saveCookies() {
        std::ofstream file(cookiesFile, std::ios::out | std::ios::trunc);
        if (!file.is_open()) return false; // IOException -> false
        std::string json = "{";
        bool first = true;
        if (cookies.has_value()) {
            for (const auto& kv : *cookies) {
                if (!first) json += ",";
                first = false;
                json += "\"" + jsonEscape(kv.first) + "\":\"" + jsonEscape(kv.second) + "\"";
            }
        }
        json += "}";
        file << json;
        file.flush();
        return !file.fail();
    }

    void setCookies(std::map<std::string, std::string>& request) {
        std::string cookiesString;
        if (cookies.has_value()) {
            for (const auto& kv : *cookies) {
                if (!cookiesString.empty()) cookiesString += "; ";
                cookiesString += kv.first + "=" + kv.second;
            }
        }
        request["cookies"] = cookiesString;
    }
};