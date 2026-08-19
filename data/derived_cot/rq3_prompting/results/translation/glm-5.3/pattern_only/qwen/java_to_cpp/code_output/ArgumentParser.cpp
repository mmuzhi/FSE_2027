#include <cctype>
#include <cerrno>
#include <climits>
#include <iostream>
#include <optional>
#include <set>
#include <string>
#include <type_traits>
#include <unordered_map>
#include <utility>
#include <variant>
#include <vector>

namespace org {
namespace example {

// Mirrors the Java Object values used by ArgumentParser: Integer, Boolean, String
using Value = std::variant<int, bool, std::string>;

enum class ArgType { Integer, Boolean, String };

template <typename X, typename Y>
struct Tuple {
    const X x;
    const Y y;
    Tuple(X x_, Y y_) : x(std::move(x_)), y(std::move(y_)) {}
};

class ArgumentParser {
public:
    std::unordered_map<std::string, Value> arguments;
    std::set<std::string> required;                       // HashSet-like
    std::unordered_map<std::string, ArgType> types;

    ArgumentParser() = default;

    Tuple<bool, std::optional<std::set<std::string>>>
    parseArguments(const std::string& commandString) {
        std::vector<std::string> args = splitOnWhitespace(commandString);
        for (int i = 1; i < static_cast<int>(args.size()); i++) {
            const std::string& arg = args[i];
            if (arg.rfind("--", 0) == 0) {                // startsWith("--")
                std::vector<std::string> keyValue = splitOnChar(arg.substr(2), '=');
                if (keyValue.size() == 2) {
                    arguments[keyValue[0]] = convertType(keyValue[0], keyValue[1]);
                } else {
                    arguments[keyValue.at(0)] = true;      // .at throws if empty (AIOOBE analog)
                }
            } else if (arg.rfind("-", 0) == 0) {           // startsWith("-")
                std::string key = arg.substr(1);
                if (i + 1 < static_cast<int>(args.size()) &&
                    args[i + 1].rfind("-", 0) != 0) {
                    arguments[key] = convertType(key, args[i + 1]);
                    i++;
                } else {
                    arguments[key] = true;
                }
            }
        }
        std::set<std::string> missingArgs = required;
        for (const auto& kv : arguments) missingArgs.erase(kv.first);
        if (!missingArgs.empty()) {
            return Tuple<bool, std::optional<std::set<std::string>>>(false, missingArgs);
        }
        return Tuple<bool, std::optional<std::set<std::string>>>(true, std::nullopt);
    }

    std::optional<Value> getArgument(const std::string& key) const {
        auto it = arguments.find(key);
        if (it == arguments.end()) return std::nullopt;    // null
        return it->second;
    }

    void addArgument(const std::string& arg, bool isRequired, ArgType argType) {
        if (isRequired) {
            required.insert(arg);
        }
        types[arg] = argType;
    }

    Value convertType(const std::string& arg, const std::string& value) const {
        auto it = types.find(arg);
        if (it != types.end()) {
            if (it->second == ArgType::Integer) {
                // Mirrors Integer.parseInt: any failure -> NumberFormatException -> return value
                const char* c = value.c_str();
                bool startsOk = !value.empty() &&
                                (c[0] == '+' || c[0] == '-' ||
                                 std::isdigit(static_cast<unsigned char>(c[0])));
                if (startsOk) {
                    errno = 0;
                    char* end = nullptr;
                    long v = std::strtol(c, &end, 10);
                    if (*end == '\0' && errno != ERANGE && v >= INT_MIN && v <= INT_MAX) {
                        return Value{static_cast<int>(v)};
                    }
                }
                return Value{value};
            } else if (it->second == ArgType::Boolean) {
                // Boolean.parseBoolean: true only for "true" ignoring case
                if (value.size() == 4) {
                    bool eq = (value[0] == 't' || value[0] == 'T') &&
                              (value[1] == 'r' || value[1] == 'R') &&
                              (value[2] == 'u' || value[2] == 'U') &&
                              (value[3] == 'e' || value[3] == 'E');
                    return Value{eq};
                }
                return Value{false};
            } else if (it->second == ArgType::String) {
                return Value{value};
            }
        }
        return Value{value};
    }

private:
    // Java String.split("\\s+"): leading whitespace yields one empty token,
    // trailing empty tokens are dropped, no-match returns the whole string.
    static std::vector<std::string> splitOnWhitespace(const std::string& s) {
        auto isWs = [](unsigned char c) {
            return c == ' ' || c == '\t' || c == '\n' || c == '\x0B' || c == '\f' || c == '\r';
        };
        std::vector<std::string> tokens;
        std::string cur;
        bool matched = false;
        size_t i = 0;
        if (!s.empty() && isWs(static_cast<unsigned char>(s[0]))) {
            tokens.push_back("");
            matched = true;
            while (i < s.size() && isWs(static_cast<unsigned char>(s[i]))) i++;
        }
        while (i < s.size()) {
            if (isWs(static_cast<unsigned char>(s[i]))) {
                tokens.push_back(cur);
                cur.clear();
                while (i < s.size() && isWs(static_cast<unsigned char>(s[i]))) i++;
            } else {
                cur += s[i++];
            }
        }
        if (!matched) return {s};
        tokens.push_back(cur);
        while (!tokens.empty() && tokens.back().empty()) tokens.pop_back();
        return tokens;
    }

    // Java String.split("=") semantics for a single-char pattern.
    static std::vector<std::string> splitOnChar(const std::string& s, char delim) {
        if (s.find(delim) == std::string::npos) return {s};
        std::vector<std::string> tokens;
        std::string cur;
        for (char c : s) {
            if (c == delim) { tokens.push_back(cur); cur.clear(); }
            else cur += c;
        }
        tokens.push_back(cur);
        while (!tokens.empty() && tokens.back().empty()) tokens.pop_back();
        return tokens;
    }
};

static std::string valueToString(const Value& v) {
    return std::visit([](const auto& x) -> std::string {
        using T = std::decay_t<decltype(x)>;
        if constexpr (std::is_same_v<T, bool>) return x ? "true" : "false";
        else if constexpr (std::is_same_v<T, int>) return std::to_string(x);
        else return x;
    }, v);
}

} // namespace example
} // namespace org

int main() {
    using org::example::ArgumentParser;
    using org::example::ArgType;

    ArgumentParser parser;
    parser.addArgument("arg1", true, ArgType::Integer);
    parser.addArgument("arg2", false, ArgType::String);
    parser.addArgument("option1", false, ArgType::Boolean);
    parser.addArgument("option2", false, ArgType::Boolean);

    auto result = parser.parseArguments(
        "python script.py --arg1=123 -arg2 value2 --option1 -option2");

    std::cout << std::boolalpha << result.x << "\n";
    if (result.y.has_value()) {
        std::cout << "[";
        bool first = true;
        for (const auto& s : *result.y) {
            if (!first) std::cout << ", ";
            std::cout << s;
            first = false;
        }
        std::cout << "]\n";
    } else {
        std::cout << "null\n";
    }

    std::cout << "{";
    bool first = true;
    for (const auto& kv : parser.arguments) {
        if (!first) std::cout << ", ";
        std::cout << kv.first << "=" << org::example::valueToString(kv.second);
        first = false;
    }
    std::cout << "}\n";
    return 0;
}