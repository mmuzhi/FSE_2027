#include <cctype>
#include <fstream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <variant>
#include <vector>

// Thrown when file content is not valid JSON (mirrors json.JSONDecodeError behavior).
class JsonError : public std::runtime_error {
public:
    explicit JsonError(const std::string& msg) : std::runtime_error(msg) {}
};

class JsonValue;
using JsonArray = std::vector<JsonValue>;
using JsonObject = std::map<std::string, JsonValue>;

// Polymorphic JSON value: null / bool / int / float / string / array / object.
class JsonValue {
public:
    using Value = std::variant<std::nullptr_t, bool, long long, double, std::string, JsonArray, JsonObject>;

    JsonValue() : value_(nullptr) {}
    JsonValue(std::nullptr_t) : value_(nullptr) {}
    JsonValue(bool b) : value_(b) {}
    JsonValue(long long n) : value_(n) {}
    JsonValue(double d) : value_(d) {}
    JsonValue(const char* s) : value_(std::string(s)) {}
    JsonValue(std::string s) : value_(std::move(s)) {}
    JsonValue(JsonArray a) : value_(std::move(a)) {}
    JsonValue(JsonObject o) : value_(std::move(o)) {}

    const Value& raw() const { return value_; }

private:
    Value value_;
};

namespace json_detail {

class Parser {
public:
    explicit Parser(const std::string& text) : s_(text) {}

    JsonValue parse() {
        skip_ws();
        JsonValue v = parse_value();
        skip_ws();
        if (pos_ != s_.size()) throw JsonError("Extra data");
        return v;
    }

private:
    const std::string& s_;
    std::size_t pos_ = 0;

    void skip_ws() {
        while (pos_ < s_.size()) {
            char c = s_[pos_];
            if (c == ' ' || c == '\t' || c == '\n' || c == '\r') ++pos_;
            else break;
        }
    }

    char peek() {
        if (pos_ >= s_.size()) throw JsonError("Expecting value");
        return s_[pos_];
    }

    JsonValue parse_value() {
        char c = peek();
        switch (c) {
            case '{': return parse_object();
            case '[': return parse_array();
            case '"': return JsonValue(parse_string());
            case 't': expect("true"); return JsonValue(true);
            case 'f': expect("false"); return JsonValue(false);
            case 'n': expect("null"); return JsonValue(nullptr);
            default: return parse_number();
        }
    }

    void expect(const char* lit) {
        for (const char* p = lit; *p; ++p) {
            if (pos_ >= s_.size() || s_[pos_] != *p) throw JsonError("Invalid literal");
            ++pos_;
        }
    }

    JsonValue parse_object() {
        ++pos_;  // '{'
        JsonObject obj;
        skip_ws();
        if (peek() == '}') { ++pos_; return JsonValue(std::move(obj)); }
        while (true) {
            skip_ws();
            if (peek() != '"') throw JsonError("Expecting property name");
            std::string key = parse_string();
            skip_ws();
            if (peek() != ':') throw JsonError("Expecting ':'");
            ++pos_;
            skip_ws();
            JsonValue val = parse_value();
            obj[std::move(key)] = std::move(val);
            skip_ws();
            char c = peek();
            if (c == ',') { ++pos_; continue; }
            if (c == '}') { ++pos_; break; }
            throw JsonError("Expecting ',' delimiter");
        }
        return JsonValue(std::move(obj));
    }

    JsonValue parse_array() {
        ++pos_;  // '['
        JsonArray arr;
        skip_ws();
        if (peek() == ']') { ++pos_; return JsonValue(std::move(arr)); }
        while (true) {
            skip_ws();
            arr.push_back(parse_value());
            skip_ws();
            char c = peek();
            if (c == ',') { ++pos_; continue; }
            if (c == ']') { ++pos_; break; }
            throw JsonError("Expecting ',' delimiter");
        }
        return JsonValue(std::move(arr));
    }

    std::string parse_string() {
        ++pos_;  // '"'
        std::string out;
        while (true) {
            if (pos_ >= s_.size()) throw JsonError("Unterminated string");
            char c = s_[pos_++];
            if (c == '"') break;
            if (c == '\\') {
                if (pos_ >= s_.size()) throw JsonError("Unterminated escape");
                char e = s_[pos_++];
                switch (e) {
                    case '"': out += '"'; break;
                    case '\\': out += '\\'; break;
                    case '/': out += '/'; break;
                    case 'b': out += '\b'; break;
                    case 'f': out += '\f'; break;
                    case 'n': out += '\n'; break;
                    case 'r': out += '\r'; break;
                    case 't': out += '\t'; break;
                    case 'u': { std::string u = parse_unicode_escape(); out += u; break; }
                    default: throw JsonError("Invalid escape");
                }
            } else {
                out += c;
            }
        }
        return out;
    }

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

    unsigned int parse_hex4() {
        if (pos_ + 4 > s_.size()) throw JsonError("Invalid \\u escape");
        unsigned int v = 0;
        for (int k = 0; k < 4; ++k) {
            char c = s_[pos_++];
            v <<= 4;
            if (c >= '0' && c <= '9') v |= static_cast<unsigned int>(c - '0');
            else if (c >= 'a' && c <= 'f') v |= static_cast<unsigned int>(c - 'a' + 10);
            else if (c >= 'A' && c <= 'F') v |= static_cast<unsigned int>(c - 'A' + 10);
            else throw JsonError("Invalid \\u escape");
        }
        return v;
    }

    std::string parse_unicode_escape() {
        unsigned int cp = parse_hex4();
        if (cp >= 0xD800 && cp <= 0xDBFF) {
            if (pos_ + 2 <= s_.size() && s_[pos_] == '\\' && s_[pos_ + 1] == 'u') {
                pos_ += 2;
                unsigned int lo = parse_hex4();
                if (lo >= 0xDC00 && lo <= 0xDFFF) {
                    cp = 0x10000 + ((cp - 0xD800) << 10) + (lo - 0xDC00);
                } else {
                    std::string out;
                    append_utf8(out, 0xFFFD);
                    append_utf8(out, lo);
                    return out;
                }
            } else {
                cp = 0xFFFD;
            }
        } else if (cp >= 0xDC00 && cp <= 0xDFFF) {
            cp = 0xFFFD;
        }
        std::string out;
        append_utf8(out, cp);
        return out;
    }

    JsonValue parse_number() {
        std::size_t start = pos_;
        bool is_float = false;
        if (peek() == '-') ++pos_;
        if (pos_ >= s_.size()) throw JsonError("Expecting value");
        if (s_[pos_] == '0') {
            ++pos_;
        } else if (std::isdigit(static_cast<unsigned char>(s_[pos_]))) {
            while (pos_ < s_.size() && std::isdigit(static_cast<unsigned char>(s_[pos_]))) ++pos_;
        } else {
            throw JsonError("Expecting value");
        }
        if (pos_ < s_.size() && s_[pos_] == '.') {
            is_float = true;
            ++pos_;
            if (pos_ >= s_.size() || !std::isdigit(static_cast<unsigned char>(s_[pos_])))
                throw JsonError("Invalid number");
            while (pos_ < s_.size() && std::isdigit(static_cast<unsigned char>(s_[pos_]))) ++pos_;
        }
        if (pos_ < s_.size() && (s_[pos_] == 'e' || s_[pos_] == 'E')) {
            is_float = true;
            ++pos_;
            if (pos_ < s_.size() && (s_[pos_] == '+' || s_[pos_] == '-')) ++pos_;
            if (pos_ >= s_.size() || !std::isdigit(static_cast<unsigned char>(s_[pos_])))
                throw JsonError("Invalid number");
            while (pos_ < s_.size() && std::isdigit(static_cast<unsigned char>(s_[pos_]))) ++pos_;
        }
        std::string num_str = s_.substr(start, pos_ - start);
        if (is_float) return JsonValue(std::stod(num_str));
        return JsonValue(static_cast<long long>(std::stoll(num_str)));
    }
};

inline JsonValue loads(const std::string& text) {
    Parser p(text);
    return p.parse();
}

}  // namespace json_detail

class TextFileProcessor {
public:
    explicit TextFileProcessor(std::string file_path) : file_path_(std::move(file_path)) {}

    // Reads the file and parses it as JSON; throws JsonError if the content
    // does not obey JSON format.
    JsonValue read_file_as_json() const {
        std::string content = read_file();
        return json_detail::loads(content);
    }

    // Reads and returns the full content of the file.
    // Throws std::runtime_error if the file cannot be opened (FileNotFoundError analog).
    std::string read_file() const {
        std::ifstream file(file_path_, std::ios::binary);
        if (!file) {
            throw std::runtime_error("[Errno 2] No such file or directory: '" + file_path_ + "'");
        }
        std::ostringstream ss;
        ss << file.rdbuf();
        // Python text mode applies universal newlines: \r\n and \r become \n.
        std::string raw = ss.str();
        std::string out;
        out.reserve(raw.size());
        for (std::size_t i = 0; i < raw.size(); ++i) {
            char c = raw[i];
            if (c == '\r') {
                if (i + 1 < raw.size() && raw[i + 1] == '\n') ++i;
                out += '\n';
            } else {
                out += c;
            }
        }
        return out;
    }

    // Writes content into the file, overwriting it if it already exists.
    void write_file(const std::string& content) const {
        std::ofstream file(file_path_, std::ios::binary | std::ios::trunc);
        if (!file) {
            throw std::runtime_error("Unable to open file for writing: '" + file_path_ + "'");
        }
        file << content;
    }

    // Reads the file, keeps only alphabetic characters, overwrites the file
    // with the processed content, and returns the processed string.
    std::string process_file() {
        std::string content = read_file();
        std::string filtered;
        filtered.reserve(content.size());
        for (char c : content) {
            if (std::isalpha(static_cast<unsigned char>(c))) filtered += c;
        }
        write_file(filtered);
        return filtered;
    }

private:
    std::string file_path_;
};