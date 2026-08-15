#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <utility>
#include <algorithm>
#include <cctype>
#include <stdexcept>

class JsonValue {
public:
    enum class Type { Null, Bool, Number, String, Array, Object };
    using JsonArray = std::vector<JsonValue>;
    using JsonObject = std::vector<std::pair<std::string, JsonValue>>;

    Type type = Type::Null;
    bool bool_value = false;
    double number_value = 0.0;
    long long int_value = 0;
    bool is_integer = false;
    std::string string_value;
    JsonArray array_value;
    JsonObject object_value;

    JsonValue() = default;
    JsonValue(bool b) : type(Type::Bool), bool_value(b) {}
    JsonValue(double d) : type(Type::Number), number_value(d), is_integer(false) {}
    JsonValue(long long i) : type(Type::Number), int_value(i), is_integer(true) {}
    JsonValue(const std::string& s) : type(Type::String), string_value(s) {}
    JsonValue(JsonArray arr) : type(Type::Array), array_value(std::move(arr)) {}
    JsonValue(JsonObject obj) : type(Type::Object), object_value(std::move(obj)) {}
};

class JsonParser {
public:
    explicit JsonParser(const std::string& text) : text(text), pos(0) {}

    JsonValue parse() {
        skip_whitespace();
        JsonValue value = parse_value();
        skip_whitespace();
        if (pos != text.size()) throw std::runtime_error("Invalid JSON: trailing characters");
        return value;
    }

private:
    const std::string& text;
    size_t pos;

    void skip_whitespace() {
        while (pos < text.size() && std::isspace(static_cast<unsigned char>(text[pos]))) ++pos;
    }

    char peek() {
        if (pos >= text.size()) throw std::runtime_error("Invalid JSON: unexpected end");
        return text[pos];
    }

    char get() {
        if (pos >= text.size()) throw std::runtime_error("Invalid JSON: unexpected end");
        return text[pos++];
    }

    JsonValue parse_value() {
        char c = peek();
        switch (c) {
            case '{': return parse_object();
            case '[': return parse_array();
            case '"': return JsonValue(parse_string());
            case 't': parse_literal("true"); return JsonValue(true);
            case 'f': parse_literal("false"); return JsonValue(false);
            case 'n': parse_literal("null"); return JsonValue();
            default:
                if (c == '-' || std::isdigit(static_cast<unsigned char>(c))) return parse_number();
                throw std::runtime_error("Invalid JSON: unexpected character");
        }
    }

    void parse_literal(const std::string& lit) {
        if (text.compare(pos, lit.size(), lit) != 0) throw std::runtime_error("Invalid JSON: invalid literal");
        pos += lit.size();
    }

    JsonValue parse_object() {
        get(); // '{'
        JsonValue::JsonObject obj;
        skip_whitespace();
        if (peek() == '}') { get(); return JsonValue(std::move(obj)); }
        while (true) {
            skip_whitespace();
            if (peek() != '"') throw std::runtime_error("Invalid JSON: expected string key");
            std::string key = parse_string();
            skip_whitespace();
            if (get() != ':') throw std::runtime_error("Invalid JSON: expected ':'");
            skip_whitespace();
            JsonValue value = parse_value();
            auto it = std::find_if(obj.begin(), obj.end(), [&](const auto& p) { return p.first == key; });
            if (it != obj.end()) it->second = std::move(value);
            else obj.emplace_back(std::move(key), std::move(value));
            skip_whitespace();
            char c = get();
            if (c == ',') continue;
            if (c == '}') break;
            throw std::runtime_error("Invalid JSON: expected ',' or '}'");
        }
        return JsonValue(std::move(obj));
    }

    JsonValue parse_array() {
        get(); // '['
        JsonValue::JsonArray arr;
        skip_whitespace();
        if (peek() == ']') { get(); return JsonValue(std::move(arr)); }
        while (true) {
            skip_whitespace();
            JsonValue value = parse_value();
            arr.push_back(std::move(value));
            skip_whitespace();
            char c = get();
            if (c == ',') continue;
            if (c == ']') break;
            throw std::runtime_error("Invalid JSON: expected ',' or ']'");
        }
        return JsonValue(std::move(arr));
    }

    std::string parse_string() {
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
                        if (pos + 4 > text.size()) throw std::runtime_error("Invalid JSON: invalid unicode escape");
                        std::string hex = text.substr(pos, 4);
                        pos += 4;
                        unsigned int codepoint = std::stoul(hex, nullptr, 16);
                        if (codepoint >= 0xD800 && codepoint <= 0xDBFF) {
                            if (pos + 6 > text.size() || text[pos] != '\\' || text[pos + 1] != 'u')
                                throw std::runtime_error("Invalid JSON: invalid surrogate pair");
                            std::string hex2 = text.substr(pos + 2, 4);
                            pos += 6;
                            unsigned int low = std::stoul(hex2, nullptr, 16);
                            if (low < 0xDC00 || low > 0xDFFF)
                                throw std::runtime_error("Invalid JSON: invalid surrogate pair");
                            codepoint = 0x10000 + ((codepoint - 0xD800) << 10) + (low - 0xDC00);
                        } else if (codepoint >= 0xDC00 && codepoint <= 0xDFFF) {
                            throw std::runtime_error("Invalid JSON: invalid unicode surrogate");
                        }
                        append_utf8(result, codepoint);
                        break;
                    }
                    default: throw std::runtime_error("Invalid JSON: invalid escape");
                }
            } else {
                if (static_cast<unsigned char>(c) < 0x20) throw std::runtime_error("Invalid JSON: control character in string");
                result += c;
            }
        }
        return result;
    }

    void append_utf8(std::string& out, unsigned int codepoint) {
        if (codepoint <= 0x7F) {
            out += static_cast<char>(codepoint);
        } else if (codepoint <= 0x7FF) {
            out += static_cast<char>(0xC0 | (codepoint >> 6));
            out += static_cast<char>(0x80 | (codepoint & 0x3F));
        } else if (codepoint <= 0xFFFF) {
            out += static_cast<char>(0xE0 | (codepoint >> 12));
            out += static_cast<char>(0x80 | ((codepoint >> 6) & 0x3F));
            out += static_cast<char>(0x80 | (codepoint & 0x3F));
        } else if (codepoint <= 0x10FFFF) {
            out += static_cast<char>(0xF0 | (codepoint >> 18));
            out += static_cast<char>(0x80 | ((codepoint >> 12) & 0x3F));
            out += static_cast<char>(0x80 | ((codepoint >> 6) & 0x3F));
            out += static_cast<char>(0x80 | (codepoint & 0x3F));
        } else {
            throw std::runtime_error("Invalid JSON: invalid unicode codepoint");
        }
    }

    JsonValue parse_number() {
        size_t start = pos;
        if (peek() == '-') get();
        if (peek() == '0') {
            get();
        } else if (std::isdigit(static_cast<unsigned char>(peek()))) {
            while (pos < text.size() && std::isdigit(static_cast<unsigned char>(text[pos]))) ++pos;
        } else {
            throw std::runtime_error("Invalid JSON: invalid number");
        }
        bool is_double = false;
        if (pos < text.size() && text[pos] == '.') {
            is_double = true;
            get();
            if (!(pos < text.size() && std::isdigit(static_cast<unsigned char>(text[pos]))))
                throw std::runtime_error("Invalid JSON: invalid number");
            while (pos < text.size() && std::isdigit(static_cast<unsigned char>(text[pos]))) ++pos;
        }
        if (pos < text.size() && (text[pos] == 'e' || text[pos] == 'E')) {
            is_double = true;
            get();
            if (pos < text.size() && (text[pos] == '+' || text[pos] == '-')) get();
            if (!(pos < text.size() && std::isdigit(static_cast<unsigned char>(text[pos]))))
                throw std::runtime_error("Invalid JSON: invalid number");
            while (pos < text.size() && std::isdigit(static_cast<unsigned char>(text[pos]))) ++pos;
        }
        std::string num_str = text.substr(start, pos - start);
        if (!is_double) {
            try {
                long long int_val = std::stoll(num_str);
                return JsonValue(int_val);
            } catch (...) {
                // fall through to double
            }
        }
        return JsonValue(std::stod(num_str));
    }
};

class TextFileProcessor {
public:
    explicit TextFileProcessor(const std::string& file_path) : file_path(file_path) {}

    JsonValue read_file_as_json() {
        std::ifstream file(file_path);
        if (!file.is_open()) throw std::runtime_error("Could not open file: " + file_path);
        std::stringstream buffer;
        buffer << file.rdbuf();
        std::string content = buffer.str();
        JsonParser parser(content);
        return parser.parse();
    }

    std::string read_file() {
        std::ifstream file(file_path);
        if (!file.is_open()) throw std::runtime_error("Could not open file: " + file_path);
        std::stringstream buffer;
        buffer << file.rdbuf();
        return buffer.str();
    }

    void write_file(const std::string& content) {
        std::ofstream file(file_path);
        if (!file.is_open()) throw std::runtime_error("Could not open file: " + file_path);
        file << content;
    }

    std::string process_file() {
        std::string content = read_file();
        std::string filtered;
        for (char c : content) {
            if (std::isalpha(static_cast<unsigned char>(c))) {
                filtered += c;
            }
        }
        write_file(filtered);
        return filtered;
    }

private:
    std::string file_path;
};