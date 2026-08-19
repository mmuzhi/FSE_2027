#include <cstdio>
#include <fstream>
#include <iterator>
#include <map>
#include <optional>
#include <stdexcept>
#include <string>

class CookiesUtil {
public:
    using Cookies = std::map<std::string, std::string>;

    explicit CookiesUtil(std::string cookies_file)
        : cookies_file_(std::move(cookies_file)) {}

    // Gets the cookies from the specified response, and saves them to cookies_file.
    // reponse: {"cookies": {key: value, ...}}; missing key throws (KeyError analog).
    void get_cookies(const std::map<std::string, Cookies>& reponse) {
        cookies_ = reponse.at("cookies");  // std::out_of_range ~ KeyError
        save_cookies();
    }

    // Loads cookies from cookies_file; {} if file not found (FileNotFoundError case).
    // Throws std::runtime_error on malformed JSON (JSONDecodeError analog).
    // Returns nullopt if the file contains JSON "null".
    std::optional<Cookies> load_cookies() {
        std::ifstream file(cookies_file_);
        if (!file.is_open()) {
            return Cookies{};  // FileNotFoundError -> {}
        }
        std::string content((std::istreambuf_iterator<char>(file)),
                            std::istreambuf_iterator<char>());
        return parse_json(content);
    }

    // Saves cookies to cookies_file; True if successful, False otherwise (bare except).
    bool save_cookies() {  // _save_cookies
        try {
            std::ofstream file(cookies_file_);
            if (!file.is_open()) {
                return false;  // open() failure -> exception in Python -> caught -> False
            }
            file << serialize(cookies_);
            return !file.fail();
        } catch (...) {
            return false;
        }
    }

    // Sets request["cookies"] to "key=value; key2=value2...".
    // If cookies is None, Python raises AttributeError -> throw here.
    void set_cookies(std::map<std::string, std::string>& request) {
        if (!cookies_.has_value()) {
            throw std::runtime_error("'NoneType' object has no attribute 'items'");
        }
        std::string joined;
        for (const auto& [key, value] : *cookies_) {
            if (!joined.empty()) joined += "; ";
            joined += key + "=" + value;
        }
        request["cookies"] = joined;
    }

    const std::optional<Cookies>& cookies() const { return cookies_; }

private:
    std::string cookies_file_;
    std::optional<Cookies> cookies_;  // None until get_cookies

    static void append_utf8(std::string& out, unsigned int cp) {
        if (cp < 0x80) {
            out += static_cast<char>(cp);
        } else if (cp < 0x800) {
            out += static_cast<char>(0xC0 | (cp >> 6));
            out += static_cast<char>(0x80 | (cp & 0x3F));
        } else if (cp < 0x10000) {
            out += static_cast<char>(0xE0 | (cp >> 12));
            out += static_cast<char>(0x80 | ((cp >> 6) & 0x3F));
            out += static_cast<char>(0x80 | (cp & 0x3F));
        } else {
            out += static_cast<char>(0xF0 | (cp >> 18));
            out += static_cast<char>(0x80 | ((cp >> 12) & 0x3F));
            out += static_cast<char>(0x80 | ((cp >> 6) & 0x3F));
            out += static_cast<char>(0x80 | (cp & 0x3F));
        }
    }

    static std::string escape(const std::string& s) {
        std::string out;
        for (char c : s) {
            switch (c) {
                case '"':  out += "\\\""; break;
                case '\\': out += "\\\\"; break;
                case '\n': out += "\\n"; break;
                case '\t': out += "\\t"; break;
                case '\r': out += "\\r"; break;
                case '\b': out += "\\b"; break;
                case '\f': out += "\\f"; break;
                default:
                    if (static_cast<unsigned char>(c) < 0x20) {
                        char buf[8];
                        std::snprintf(buf, sizeof(buf), "\\u%04x", c);
                        out += buf;
                    } else {
                        out += c;
                    }
            }
        }
        return out;
    }

    // Matches json.dump default format: {"k": "v", "k2": "v2"}; None -> null
    static std::string serialize(const std::optional<Cookies>& cookies) {
        if (!cookies.has_value()) return "null";
        std::string out = "{";
        bool first = true;
        for (const auto& [k, v] : *cookies) {
            if (!first) out += ", ";
            first = false;
            out += "\"" + escape(k) + "\": \"" + escape(v) + "\"";
        }
        out += "}";
        return out;
    }

    static void skip_ws(const std::string& s, size_t& i) {
        while (i < s.size() &&
               (s[i] == ' ' || s[i] == '\t' || s[i] == '\n' || s[i] == '\r')) {
            ++i;
        }
    }

    static std::string parse_string(const std::string& s, size_t& i) {
        if (i >= s.size() || s[i] != '"') throw std::runtime_error("Invalid JSON");
        ++i;
        std::string out;
        while (i < s.size() && s[i] != '"') {
            if (s[i] == '\\') {
                ++i;
                if (i >= s.size()) throw std::runtime_error("Invalid JSON");
                switch (s[i]) {
                    case 'n': out += '\n'; break;
                    case 't': out += '\t'; break;
                    case 'r': out += '\r'; break;
                    case 'b': out += '\b'; break;
                    case 'f': out += '\f'; break;
                    case '"': out += '"';  break;
                    case '\\': out += '\\'; break;
                    case '/': out += '/';  break;
                    case 'u': {
                        if (i + 4 >= s.size()) throw std::runtime_error("Invalid JSON");
                        unsigned int cp = 0;
                        for (int k = 1; k <= 4; ++k) {
                            char h = s[i + k];
                            cp <<= 4;
                            if (h >= '0' && h <= '9') cp |= static_cast<unsigned>(h - '0');
                            else if (h >= 'a' && h <= 'f') cp |= static_cast<unsigned>(h - 'a' + 10);
                            else if (h >= 'A' && h <= 'F') cp |= static_cast<unsigned>(h - 'A' + 10);
                            else throw std::runtime_error("Invalid JSON");
                        }
                        i += 4;
                        append_utf8(out, cp);
                        break;
                    }
                    default: throw std::runtime_error("Invalid JSON");
                }
                ++i;
            } else {
                out += s[i++];
            }
        }
        if (i >= s.size()) throw std::runtime_error("Invalid JSON");
        ++i;  // closing quote
        return out;
    }

    static std::optional<Cookies> parse_json(const std::string& s) {
        size_t i = 0;
        skip_ws(s, i);
        if (s.compare(i, 4, "null") == 0) return std::nullopt;
        if (i >= s.size() || s[i] != '{') throw std::runtime_error("Invalid JSON");
        ++i;
        Cookies cookies;
        skip_ws(s, i);
        if (i < s.size() && s[i] == '}') { ++i; return cookies; }
        while (true) {
            skip_ws(s, i);
            std::string key = parse_string(s, i);
            skip_ws(s, i);
            if (i >= s.size() || s[i] != ':') throw std::runtime_error("Invalid JSON");
            ++i;
            skip_ws(s, i);
            std::string value = parse_string(s, i);
            cookies[key] = value;
            skip_ws(s, i);
            if (i < s.size() && s[i] == ',') { ++i; continue; }
            if (i < s.size() && s[i] == '}') { ++i; break; }
            throw std::runtime_error("Invalid JSON");
        }
        return cookies;
    }
};