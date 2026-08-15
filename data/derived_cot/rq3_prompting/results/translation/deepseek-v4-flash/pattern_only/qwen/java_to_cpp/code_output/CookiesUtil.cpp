#include <cctype>
#include <cstdio>
#include <exception>
#include <fstream>
#include <map>
#include <optional>
#include <sstream>
#include <string>

class JsonParseException : public std::exception {
public:
    explicit JsonParseException(const std::string& msg) : msg_(msg) {}
    const char* what() const noexcept override { return msg_.c_str(); }
private:
    std::string msg_;
};

class TypeMismatchException : public std::exception {
public:
    explicit TypeMismatchException(const std::string& msg) : msg_(msg) {}
    const char* what() const noexcept override { return msg_.c_str(); }
private:
    std::string msg_;
};

class CookiesUtil {
public:
    CookiesUtil(const std::string& cookiesFile)
        : cookiesFile_(cookiesFile), cookies_(std::nullopt) {}

    void getCookies(std::map<std::string, std::map<std::string, std::string>>& response) {
        auto it = response.find("cookies");
        if (it != response.end()) {
            cookies_ = it->second;
        } else {
            cookies_ = std::nullopt;
        }
        _saveCookies();
    }

    std::map<std::string, std::string> loadCookies() {
        std::ifstream file(cookiesFile_, std::ios::binary);
        if (!file.is_open()) {
            return {};
        }
        std::stringstream buffer;
        buffer << file.rdbuf();
        if (file.bad()) {
            return {};
        }
        try {
            return parseObject(buffer.str());
        } catch (const JsonParseException&) {
            return {};
        }
    }

    void setCookies(std::map<std::string, std::string>& request) {
        std::string cookiesString;
        if (cookies_) {
            for (const auto& [key, value] : *cookies_) {
                if (!cookiesString.empty()) {
                    cookiesString += "; ";
                }
                cookiesString += key;
                cookiesString += "=";
                cookiesString += value;
            }
        }
        request["cookies"] = cookiesString;
    }

private:
    bool _saveCookies() {
        std::ofstream file(cookiesFile_, std::ios::binary);
        if (!file.is_open()) {
            return false;
        }
        std::string json;
        if (cookies_) {
            json = writeObject(*cookies_);
        } else {
            json = "{}";
        }
        file << json;
        file.flush();
        return file.good();
    }

    std::string cookiesFile_;
    std::optional<std::map<std::string, std::string>> cookies_;

    static std::string writeObject(const std::map<std::string, std::string>& obj) {
        std::string out = "{";
        bool first = true;
        for (const auto& [key, value] : obj) {
            if (!first) out += ",";
            first = false;
            out += escapeString(key);
            out += ":";
            out += escapeString(value);
        }
        out += "}";
        return out;
    }

    static std::string escapeString(const std::string& s) {
        std::string out;
        out.reserve(s.size() + 2);
        out += '"';
        size_t i = 0;
        while (i < s.size()) {
            unsigned int cp;
            size_t len;
            unsigned char c = static_cast<unsigned char>(s[i]);
            if (c < 0x80) {
                cp = c;
                len = 1;
            } else if ((c >> 5) == 0x6) {
                if (i + 1 >= s.size()) { cp = 0xFFFD; len = 1; }
                else {
                    cp = ((c & 0x1F) << 6) | (static_cast<unsigned char>(s[i + 1]) & 0x3F);
                    len = 2;
                }
            } else if ((c >> 4) == 0xE) {
                if (i + 2 >= s.size()) { cp = 0xFFFD; len = 1; }
                else {
                    cp = ((c & 0x0F) << 12) |
                         ((static_cast<unsigned char>(s[i + 1]) & 0x3F) << 6) |
                         (static_cast<unsigned char>(s[i + 2]) & 0x3F);
                    len = 3;
                }
            } else if ((c >> 3) == 0x1E) {
                if (i + 3 >= s.size()) { cp = 0xFFFD; len = 1; }
                else {
                    cp = ((c & 0x07) << 18) |
                         ((static_cast<unsigned char>(s[i + 1]) & 0x3F) << 12) |
                         ((static_cast<unsigned char>(s[i + 2]) & 0x3F) << 6) |
                         (static_cast<unsigned char>(s[i + 3]) & 0x3F);
                    len = 4;
                }
            } else {
                cp = 0xFFFD;
                len = 1;
            }

            switch (cp) {
                case '"': out += "\\\""; break;
                case '\\': out += "\\\\"; break;
                case '\b': out += "\\b"; break;
                case '\f': out += "\\f"; break;
                case '\n': out += "\\n"; break;
                case '\r': out += "\\r"; break;
                case '\t': out += "\\t"; break;
                case '/': out += "\\/"; break;
                default:
                    if (cp <= 0x1F || (cp >= 0x7F && cp <= 0x9F) || (cp >= 0x2000 && cp <= 0x20FF)) {
                        char buf[7];
                        snprintf(buf, sizeof(buf), "\\u%04X", cp);
                        out += buf;
                    } else {
                        out += encodeUtf8(cp);
                    }
            }
            i += len;
        }
        out += '"';
        return out;
    }

    static std::string encodeUtf8(unsigned int cp) {
        std::string out;
        if (cp <= 0x7F) {
            out += static_cast<char>(cp);
        } else if (cp <= 0x7FF) {
            out += static_cast<char>(0xC0 | (cp >> 6));
            out += static_cast<char>(0x80 | (cp & 0x3F));
        } else if (cp <= 0xFFFF) {
            out += static_cast<char>(0xE0 | (cp >> 12));
            out += static_cast<char>(0x80 | ((cp >> 6) & 0x3F));
            out += static_cast<char>(0x80 | (cp & 0x3F));
        } else if (cp <= 0x10FFFF) {
            out += static_cast<char>(0xF0 | (cp >> 18));
            out += static_cast<char>(0x80 | ((cp >> 12) & 0x3F));
            out += static_cast<char>(0x80 | ((cp >> 6) & 0x3F));
            out += static_cast<char>(0x80 | (cp & 0x3F));
        } else {
            out += "?";
        }
        return out;
    }

    static std::map<std::string, std::string> parseObject(const std::string& text) {
        size_t pos = 0;
        skipWhitespace(text, pos);
        if (pos >= text.size()) {
            throw JsonParseException("Empty input");
        }
        char first = text[pos];
        if (first != '{') {
            if (first == '"' || first == '[' || first == 't' || first == 'f' || first == 'n' ||
                first == '-' || (first >= '0' && first <= '9')) {
                throw TypeMismatchException("Not a JSON object");
            } else {
                throw JsonParseException("Invalid JSON");
            }
        }
        pos++;
        std::map<std::string, std::string> result;
        skipWhitespace(text, pos);
        if (pos < text.size() && text[pos] == '}') {
            pos++;
            skipWhitespace(text, pos);
            if (pos != text.size()) throw JsonParseException("Trailing characters");
            return result;
        }
        while (true) {
            skipWhitespace(text, pos);
            if (pos >= text.size()) throw JsonParseException("Unexpected end");
            if (text[pos] != '"') throw JsonParseException("Expected string key");
            std::string key = parseString(text, pos);
            skipWhitespace(text, pos);
            if (pos >= text.size() || text[pos] != ':') throw JsonParseException("Expected ':'");
            pos++;
            skipWhitespace(text, pos);
            if (pos >= text.size()) throw JsonParseException("Unexpected end");
            if (text[pos] != '"') throw TypeMismatchException("Value is not a string");
            std::string value = parseString(text, pos);
            result[key] = value;
            skipWhitespace(text, pos);
            if (pos >= text.size()) throw JsonParseException("Unexpected end");
            char c = text[pos];
            pos++;
            if (c == ',') continue;
            if (c == '}') break;
            throw JsonParseException("Expected ',' or '}'");
        }
        skipWhitespace(text, pos);
        if (pos != text.size()) throw JsonParseException("Trailing characters");
        return result;
    }

    static void skipWhitespace(const std::string& s, size_t& pos) {
        while (pos < s.size() && (s[pos] == ' ' || s[pos] == '\t' || s[pos] == '\n' || s[pos] == '\r')) {
            pos++;
        }
    }

    static std::string parseString(const std::string& s, size_t& pos) {
        if (s[pos] != '"') throw JsonParseException("Expected string");
        pos++;
        std::string out;
        while (true) {
            if (pos >= s.size()) throw JsonParseException("Unterminated string");
            char c = s[pos];
            if (c == '"') {
                pos++;
                break;
            }
            if (c == '\\') {
                pos++;
                if (pos >= s.size()) throw JsonParseException("Unterminated escape");
                char e = s[pos];
                pos++;
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
                        if (pos + 4 > s.size()) throw JsonParseException("Invalid unicode escape");
                        std::string hex = s.substr(pos, 4);
                        for (char h : hex) {
                            if (!isxdigit(static_cast<unsigned char>(h))) throw JsonParseException("Invalid unicode escape");
                        }
                        unsigned int cp = std::stoul(hex, nullptr, 16);
                        pos += 4;
                        if (cp >= 0xD800 && cp <= 0xDBFF) {
                            if (pos + 6 <= s.size() && s[pos] == '\\' && s[pos + 1] == 'u') {
                                std::string hex2 = s.substr(pos + 2, 4);
                                bool valid = true;
                                for (char h : hex2) {
                                    if (!isxdigit(static_cast<unsigned char>(h))) { valid = false; break; }
                                }
                                if (valid) {
                                    unsigned int low = std::stoul(hex2, nullptr, 16);
                                    if (low >= 0xDC00 && low <= 0xDFFF) {
                                        cp = 0x10000 + ((cp - 0xD800) << 10) + (low - 0xDC00);
                                        pos += 6;
                                        out += encodeUtf8(cp);
                                        break;
                                    }
                                }
                            }
                            out += '?';
                        } else if (cp >= 0xDC00 && cp <= 0xDFFF) {
                            out += '?';
                        } else {
                            out += encodeUtf8(cp);
                        }
                        break;
                    }
                    default:
                        throw JsonParseException("Invalid escape");
                }
            } else {
                if (static_cast<unsigned char>(c) < 0x20) {
                    throw JsonParseException("Unescaped control character");
                }
                out += c;
                pos++;
            }
        }
        return out;
    }
};