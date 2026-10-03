#include <string>
#include <map>
#include <set>
#include <vector>
#include <sstream>
#include <any>
#include <functional>
#include <optional>
#include <algorithm>
#include <stdexcept>

class ArgumentParser {
public:
    ArgumentParser() = default;

    std::pair<bool, std::optional<std::set<std::string>>> parse_arguments(const std::string& command_string) {
        std::vector<std::string> args;
        std::istringstream iss(command_string);
        std::string token;
        while (iss >> token) {
            args.push_back(token);
        }

        for (size_t i = 1; i < args.size(); ++i) {
            const std::string& arg = args[i];
            if (arg.rfind("--", 0) == 0) {
                std::string key_value_str = arg.substr(2);
                std::vector<std::string> key_value;
                std::string current;
                for (char c : key_value_str) {
                    if (c == '=') {
                        key_value.push_back(current);
                        current.clear();
                    } else {
                        current += c;
                    }
                }
                key_value.push_back(current);

                if (key_value.size() == 2) {
                    arguments[key_value[0]] = _convert_type(key_value[0], key_value[1]);
                } else {
                    arguments[key_value[0]] = true;
                }
            } else if (arg.rfind("-", 0) == 0) {
                std::string key = arg.substr(1);
                if (i + 1 < args.size() && (args[i + 1].empty() || args[i + 1][0] != '-')) {
                    arguments[key] = _convert_type(key, args[i + 1]);
                } else {
                    arguments[key] = true;
                }
            }
        }

        std::set<std::string> arg_keys;
        for (const auto& pair : arguments) {
            arg_keys.insert(pair.first);
        }

        std::set<std::string> missing_args;
        std::set_difference(required.begin(), required.end(),
                            arg_keys.begin(), arg_keys.end(),
                            std::inserter(missing_args, missing_args.begin()));

        if (!missing_args.empty()) {
            return {false, missing_args};
        }

        return {true, std::nullopt};
    }

    std::any get_argument(const std::string& key) const {
        auto it = arguments.find(key);
        if (it != arguments.end()) {
            return it->second;
        }
        return {};
    }

    void add_argument(const std::string& arg, bool required = false, 
                      std::function<std::any(const std::string&)> arg_type = default_type) {
        if (required) {
            this->required.insert(arg);
        }
        types[arg] = arg_type;
    }

private:
    std::map<std::string, std::any> arguments;
    std::set<std::string> required;
    std::map<std::string, std::function<std::any(const std::string&)>> types;

    static std::any default_type(const std::string& value) {
        return value;
    }

    std::any _convert_type(const std::string& arg, const std::string& value) {
        auto it = types.find(arg);
        if (it != types.end()) {
            try {
                return it->second(value);
            } catch (const std::invalid_argument&) {
                return value;
            }
        }
        return value;
    }
};