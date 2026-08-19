#include <map>
#include <optional>
#include <set>
#include <sstream>
#include <string>
#include <utility>
#include <variant>
#include <vector>
#include <stdexcept>

class ArgumentParser {
public:
    // Python values here are: str, bool True, or converted types (int, float, ...)
    using Value = std::variant<std::string, bool, long long, double>;
    // (True, None) or (False, missing_args)
    using ParseResult = std::pair<bool, std::optional<std::set<std::string>>>;

    ArgumentParser() = default;

    ParseResult parse_arguments(const std::string& command_string) {
        // Equivalent of Python str.split(): split on whitespace, no empty tokens.
        std::vector<std::string> tokens;
        {
            std::istringstream iss(command_string);
            std::string tok;
            while (iss >> tok) tokens.push_back(tok);
        }

        // args = command_string.split()[1:]
        std::vector<std::string> args;
        if (tokens.size() > 1)
            args.assign(tokens.begin() + 1, tokens.end());

        for (std::size_t i = 0; i < args.size(); ++i) {
            const std::string& arg = args[i];
            if (arg.rfind("--", 0) == 0) {
                std::vector<std::string> key_value = split(arg.substr(2), '=');
                if (key_value.size() == 2)
                    arguments[key_value[0]] = _convert_type(key_value[0], key_value[1]);
                else
                    arguments[key_value[0]] = true;
            } else if (!arg.empty() && arg[0] == '-') {
                const std::string key = arg.substr(1);
                if (i + 1 < args.size() &&
                    (args[i + 1].empty() || args[i + 1][0] != '-'))
                    arguments[key] = _convert_type(key, args[i + 1]);
                else
                    arguments[key] = true;
            }
        }

        // missing_args = self.required - set(self.arguments.keys())
        std::set<std::string> missing_args;
        for (const std::string& r : required)
            if (arguments.find(r) == arguments.end())
                missing_args.insert(r);

        if (!missing_args.empty())
            return {false, missing_args};
        return {true, std::nullopt};
    }

    std::optional<Value> get_argument(const std::string& key) const {
        auto it = arguments.find(key);
        if (it == arguments.end()) return std::nullopt;
        return it->second;
    }

    void add_argument(const std::string& arg, bool required = false,
                      const std::string& arg_type = "str") {
        if (required) this->required.insert(arg);
        types[arg] = arg_type;
    }

    Value _convert_type(const std::string& arg, const std::string& value) const {
        auto it = types.find(arg);
        if (it == types.end() || it->second == "str")
            return value;  // KeyError path / str(value) is identity for str input
        const std::string& t = it->second;
        try {
            std::size_t pos = 0;
            if (t == "int" || t == "long" || t == "long long") {
                long long v = std::stoll(value, &pos);
                if (pos == value.size()) return v;
                return value;  // trailing junk -> ValueError in Python
            }
            if (t == "float" || t == "double") {
                double v = std::stod(value, &pos);
                if (pos == value.size()) return v;
                return value;
            }
            if (t == "bool")
                return !value.empty();  // bool(non-empty str) is True in Python
            return value;  // unknown type tag: behave like identity
        } catch (const std::exception&) {
            return value;  // ValueError -> return original value
        }
    }

    std::map<std::string, Value> arguments;
    std::set<std::string> required;
    std::map<std::string, std::string> types;

private:
    // Equivalent of Python str.split(char) with no maxsplit (empty fields kept).
    static std::vector<std::string> split(const std::string& s, char delim) {
        std::vector<std::string> parts;
        std::string cur;
        for (char c : s) {
            if (c == delim) { parts.push_back(cur); cur.clear(); }
            else cur.push_back(c);
        }
        parts.push_back(cur);
        return parts;
    }
};