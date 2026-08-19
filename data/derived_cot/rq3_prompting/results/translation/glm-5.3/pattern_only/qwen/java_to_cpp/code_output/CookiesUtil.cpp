#include <fstream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>

namespace org {
namespace example {

namespace {

// Analog of org.json.simple.parser.ParseException: malformed JSON.
class JsonParseException : public std::runtime_error {
public:
    explicit JsonParseException(const std::string& msg) : std::runtime_error(msg) {}
};

// Analog of the (uncaught) java.lang.ClassCastException raised when a parsed
// JSON value cannot be used as java.lang.String / org.json.simple.JSONObject.
class JsonCastException : public std::runtime_error {
public:
    explicit JsonCastException(const std::string& msg) : std::runtime_error(msg) {}
};

// Escapes a string the way org.json.simple.JSONValue.escape does.
std::string jsonEscape(const std::string& s) {
    static const char* hex = "0123456789ABCDEF";
    std::string out;
    out.reserve(s.size());
    for (std::string::size_type i = 0; i < s.size(); ++i) {
        unsigned char ch = static_cast<unsigned char>(s[i]);
        switch (ch) {
            case '"':  out += "\\\""; break;
            case '\\': out += "\\\\"; break;
            case '\b': out += "\\b"; break;
            case '\f': out += "\\f"; break;
            case '\n': out += "\\n"; break;
            case '\r': out += "\\r"; break;
            case '\t': out += "\\t"; break;
            default:
                // Control characters are emitted as \uXXXX (uppercase hex).
                if (ch <= 0x1F || (ch >= 0x7F && ch <= 0x9F)) {
                    out += "\\u00";
                    out += hex[(ch >> 4) & 0xF];
                    out += hex[ch & 0xF];
                } else {
                    out += static_cast<char>(ch);
                }
        }
    }
    return out;
}

// Minimal JSON reader replicating the observable behavior of
// org.json.simple.parser.JSONParser for this class's usage pattern:
//  - malformed input                       -> JsonParseException (recoverable)
//  - non-object top level / non-string values -> JsonCastException (propagates)
//  - duplicate keys: the later value wins (HashMap.put semantics)
class JsonParser {
public:
    explicit JsonParser(const std::string& text) : text_(text), pos_(0) {}

    std::map<std::string, std::string> parseDocument() {
        skipWhitespace();
        if (pos_ >= text_.size()) throw JsonParseException("unexpected end of input");
        if (text_[pos_] == '{') return parseObject();
        parseValue();  // validate an alternative top-level value, then fail the cast
        throw JsonCastException("org.json.simple.JSONObject cannot be cast");
    }

private:
    std::map<std::string, std::string> parseObject() {
        std::map<std::string, std::string> result;
        bool allValuesStrings = true;
        expect('{');
        skipWhitespace();
        if (peek() == '}') {
            ++pos_;
        } else {
            while (true) {
                skipWhitespace();
                if (peek() != '"') throw JsonParseException("expected object key");
                std::string key = parseString();
                skipWhitespace();
                expect(':');
                skipWhitespace();
                if (peek() == '"') {
                    result[key] = parseString();
                } else {
                    parseValue();  // validate/skip; value is not a java.lang.String
                    allValuesStrings = false;
                }
                skipWhitespace();
                char c = nextChar();
                if (c == '}') break;
                if (c != ',') throw JsonParseException("expected ',' or '}'");
            }
        }
        if (!allValuesStrings) {
            throw JsonCastException("java.lang.String cannot be cast");
        }
        return result;
    }

    void parseValue() {
        skipWhitespace();
        char c = peek();
        if (c == '"') { parseString(); return; }
        if (c == '{') { skipObject(); return; }
        if (c == '[') { skipArray(); return; }
        if (c == 't') { expectWord("true"); return; }
        if (c == 'f') { expectWord("false"); return; }
        if (c == 'n') { expectWord("null"); return; }
        if (c == '-' || (c >= '0' && c <= '9')) { skipNumber(); return; }
        throw JsonParseException("unexpected character");
    }

    std::string parseString() {
        expect('"');
        std::string out;
        while (true) {
            char c = nextChar();
            if (c == '"') return out;
            if (c == '\\') {
                char e = nextChar();
                switch (e) {
                    case '"':  out += '"';  break;
                    case '\\': out += '\\'; break;
                    case '/':  out += '/';  break;
                    case 'b':  out += '\b'; break;
                    case 'f':  out += '\f'; break;
                    case 'n':  out += '\n'; break;
                    case 'r':  out += '\r'; break;
                    case 't':  out += '\t'; break;
                    case 'u': {
                        unsigned v = 0;
                        for (int k = 0; k < 4; ++k) {
                            char h = nextChar();
                            v <<= 4;
                            if (h >= '0' && h <= '9')      v |= static_cast<unsigned>(h - '0');
                            else if (h >= 'a' && h <= 'f') v |= static_cast<unsigned>(h - 'a' + 10);
                            else if (h >= 'A' && h <= 'F') v |= static_cast<unsigned>(h - 'A' + 10);
                            else throw JsonParseException("invalid unicode escape");
                        }
                        if (v < 0x80) {
                            out += static_cast<char>(v);
                        } else if (v < 0x800) {
                            out += static_cast<char>(0xC0 | (v >> 6));
                            out += static_cast<char>(0x80 | (v & 0x3F));
                        } else {
                            out += static_cast<char>(0xE0 | (v >> 12));
                            out += static_cast<char>(0x80 | ((v >> 6) & 0x3F));
                            out += static_cast<char>(0x80 | (v & 0x3F));
                        }
                        break;
                    }
                    default: throw JsonParseException("invalid escape");
                }
            } else {
                out += c;
            }
        }
    }

    void skipObject() {
        expect('{');
        skipWhitespace();
        if (peek() == '}') { ++pos_; return; }
        while (true) {
            skipWhitespace();
            if (peek() != '"') throw JsonParseException("expected object key");
            parseString();
            skipWhitespace();
            expect(':');
            parseValue();
            skipWhitespace();
            char c = nextChar();
            if (c == '}') return;
            if (c != ',') throw JsonParseException("expected ',' or '}'");
        }
    }

    void skipArray() {
        expect('[');
        skipWhitespace();
        if (peek() == ']') { ++pos_; return; }
        while (true) {
            parseValue();
            skipWhitespace();
            char c = nextChar();
            if (c == ']') return;
            if (c != ',') throw JsonParseException("expected ',' or ']'");
        }
    }

    void expectWord(const char* w) {
        for (const char* p = w; *p != '\0'; ++p) {
            if (pos_ >= text_.size() || text_[pos_] != *p)
                throw JsonParseException("invalid literal");
            ++pos_;
        }
    }

    void skipNumber() {
        std::string::size_type start = pos_;
        if (peek() == '-') ++pos_;
        while (pos_ < text_.size()) {
            char c = text_[pos_];
            if ((c >= '0' && c <= '9') || c == '.' || c == 'e' || c == 'E' || c == '+' || c == '-') ++pos_;
            else break;
        }
        if (pos_ == start) throw JsonParseException("invalid number");
    }

    void expect(char c) {
        if (pos_ >= text_.size() || text_[pos_] != c)
            throw JsonParseException(std::string("expected '") + c + "'");
        ++pos_;
    }

    char peek() const { return pos_ < text_.size() ? text_[pos_] : '\0'; }

    char nextChar() {
        if (pos_ >= text_.size()) throw JsonParseException("unexpected end of input");
        return text_[pos_++];
    }

    void skipWhitespace() {
        while (pos_ < text_.size()) {
            char c = text_[pos_];
            if (c == ' ' || c == '\t' || c == '\n' || c == '\r') ++pos_;
            else break;
        }
    }

    const std::string& text_;
    std::string::size_type pos_;
};

}  // namespace

class CookiesUtil {
public:
    typedef std::map<std::string, std::string> CookiesMap;
    typedef std::map<std::string, CookiesMap> ResponseMap;

    explicit CookiesUtil(std::string cookiesFile)
        : cookiesFile(std::move(cookiesFile)), cookies(nullptr) {}

    void getCookies(ResponseMap& response) {
        ResponseMap::iterator it = response.find("cookies");
        this->cookies = (it != response.end()) ? &it->second : nullptr;
        _saveCookies();
    }

    CookiesMap loadCookies() {
        std::ifstream reader(cookiesFile.c_str(), std::ios::in | std::ios::binary);
        if (!reader.is_open()) {
            return CookiesMap();  // IOException path (e.g. missing file)
        }
        std::ostringstream buffer;
        buffer << reader.rdbuf();
        try {
            return JsonParser(buffer.str()).parseDocument();
        } catch (const JsonParseException&) {
            return CookiesMap();  // ParseException path
        }
        // JsonCastException propagates, like the uncaught ClassCastException.
    }

    bool _saveCookies() {
        std::ofstream file(cookiesFile.c_str(), std::ios::out | std::ios::binary | std::ios::trunc);
        if (!file.is_open()) {
            return false;  // IOException from the FileWriter constructor
        }
        std::string json = "{";
        bool first = true;
        if (cookies != nullptr) {
            for (CookiesMap::const_iterator it = cookies->begin(); it != cookies->end(); ++it) {
                if (!first) json += ",";
                first = false;
                json += "\"";
                json += jsonEscape(it->first);
                json += "\":\"";
                json += jsonEscape(it->second);
                json += "\"";
            }
        }
        json += "}";
        file << json;
        file.flush();
        return file.good();
    }

    void setCookies(CookiesMap& request) {
        std::string cookiesString;
        if (cookies != nullptr) {
            for (CookiesMap::const_iterator it = cookies->begin(); it != cookies->end(); ++it) {
                if (!cookiesString.empty()) {
                    cookiesString += "; ";
                }
                cookiesString += it->first;
                cookiesString += "=";
                cookiesString += it->second;
            }
        }
        request["cookies"] = cookiesString;
    }

private:
    std::string cookiesFile;
    CookiesMap* cookies;  // nullable reference, mirrors the Java Map reference
};

}  // namespace example
}  // namespace org