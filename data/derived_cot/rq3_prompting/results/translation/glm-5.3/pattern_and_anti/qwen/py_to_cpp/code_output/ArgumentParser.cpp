#include <algorithm>
#include <cctype>
#include <iterator>
#include <map>
#include <optional>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <variant>
#include <vector>

// Python-type value: None (monostate), bool, int, float, or str
using PyValue = std::variant<std::monostate, bool, long long, double, std::string>;

class ArgumentParser {
public:
    enum class ArgType { Str, Int, Float, Bool };

    ArgumentParser() = default;

    // Parses the command line argument string.
    // Returns (true, nullopt) on success; (false, missing_args) if required args are missing.
    std::pair<bool, std::optional<std::set<std::string>>>
    parse_arguments(const std::string& command_string) {
        std::vector<std::string> args = split_ws(command_string);
        if (!args.empty()) args.erase(args.begin());  // skip program name: split()[1:]

        for (std::size_t i = 0; i < args.size(); ++i) {
            const std::string& arg = args[i];
            if (starts_with(arg, "--")) {
                std::vector<std::string> kv = split_all(arg.substr(2), '=');
                if (kv.size() == 2)
                    arguments[kv[0]] = _convert_type(kv[0], kv[1]);
                else
                    arguments[kv[0]] = true;
            } else if (starts_with(arg, "-")) {
                std::string key = arg.substr(1);
                if (i + 1 < args.size() && !starts_with(args[i + 1], "-"))
                    arguments[key] = _convert_type(key, args[i + 1]);
                else
                    arguments[key] = true;
            }
        }

        std::set<std::string> keys;
        for (const auto& kv : arguments) keys.insert(kv.first);
        std::set<std::string> missing;
        std::set_difference(required.begin(), required.end(),
                            keys.begin(), keys.end(),
                            std::inserter(missing, missing.begin()));
        if (!missing.empty())
            return {false, missing};
        return {true, std::nullopt};
    }

    // Returns the argument value, or None (monostate) if the argument does not exist.
    PyValue get_argument(const std::string& key) const {
        auto it = arguments.find(key);
        if (it == arguments.end()) return std::monostate{};
        return it->second;
    }

    void add_argument(const std::string& arg, bool required_ = false,
                      ArgType arg_type = ArgType::Str) {
        if (required_) required.insert(arg);
        types[arg] = arg_type;
    }

    // Tries to convert the value using self.types; returns the original
    // string on KeyError (unknown arg) or ValueError (failed conversion).
    PyValue _convert_type(const std::string& arg, const std::string& value) const {
        auto it = types.find(arg);
        if (it == types.end()) return value;  // KeyError -> value
        try {
            switch (it->second) {
                case ArgType::Int:   return to_int(value);
                case ArgType::Float: return to_float(value);
                case ArgType::Bool:  return true;  // bool(x) never fails
                default:             return value; // str(x)
            }
        } catch (const std::invalid_argument&) {   // ValueError
            return value;
        } catch (const std::out_of_range&) {       // ValueError
            return value;
        }
    }

private:
    std::map<std::string, PyValue> arguments;
    std::set<std::string> required;
    std::map<std::string, ArgType> types;

    static bool starts_with(const std::string& s, const char* p) {
        return s.rfind(p, 0) == 0;
    }

    // Equivalent of Python str.split() (any whitespace, no empty tokens)
    static std::vector<std::string> split_ws(const std::string& s) {
        std::vector<std::string> out;
        std::istringstream iss(s);
        std::string t;
        while (iss >> t) out.push_back(t);
        return out;
    }

    // Equivalent of Python str.split(sep): split on every occurrence, keep empties
    static std::vector<std::string> split_all(const std::string& s, char sep) {
        std::vector<std::string> out;
        std::string cur;
        for (char c : s) {
            if (c == sep) { out.push_back(cur); cur.clear(); }
            else cur += c;
        }
        out.push_back(cur);
        return out;
    }

    static PyValue to_int(const std::string& s) {
        std::size_t pos = 0;
        long long v = std::stoll(s, &pos);
        while (pos < s.size() && std::isspace(static_cast<unsigned char>(s[pos]))) ++pos;
        if (pos != s.size()) throw std::invalid_argument("invalid int literal");
        return v;
    }

    static PyValue to_float(const std::string& s) {
        std::size_t pos = 0;
        double v = std::stod(s, &pos);
        while (pos < s.size() && std::isspace(static_cast<unsigned char>(s[pos]))) ++pos;
        if (pos != s.size()) throw std::invalid_argument("invalid float literal");
        return v;
    }
};