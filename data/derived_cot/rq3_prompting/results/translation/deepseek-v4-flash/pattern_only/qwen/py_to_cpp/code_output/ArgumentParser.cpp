#include <any>
#include <functional>
#include <map>
#include <optional>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

class ArgumentParser {
public:
    std::map<std::string, std::any> arguments;
    std::set<std::string> required;
    std::map<std::string, std::function<std::any(const std::string&)>> types;

    ArgumentParser() {}

    std::pair<bool, std::optional<std::set<std::string>>> parse_arguments(const std::string& command_string) {
        std::istringstream iss(command_string);
        std::vector<std::string> args;
        std::string token;
        while (iss >> token) {
            args.push_back(token);
        }

        for (size_t i = 1; i < args.size(); ++i) {
            const std::string& arg = args[i];

            if (arg.rfind("--", 0) == 0) {
                std::string body = arg.substr(2);
                size_t eq = body.find('=');
                size_t eq2 = (eq == std::string::npos) ? std::string::npos : body.find('=', eq + 1);

                if (eq != std::string::npos && eq2 == std::string::npos) {
                    std::string key = body.substr(0, eq);
                    std::string value = body.substr(eq + 1);
                    arguments[key] = _convert_type(key, value);
                } else {
                    std::string key = (eq == std::string::npos) ? body : body.substr(0, eq);
                    arguments[key] = true;
                }
            } else if (arg.rfind("-", 0) == 0) {
                std::string key = arg.substr(1);
                if (i + 1 < args.size() && args[i + 1].rfind("-", 0) != 0) {
                    arguments[key] = _convert_type(key, args[i + 1]);
                    ++i;
                } else {
                    arguments[key] = true;
                }
            }
        }

        std::set<std::string> missing_args;
        for (const auto& r : required) {
            if (arguments.find(r) == arguments.end()) {
                missing_args.insert(r);
            }
        }

        if (!missing_args.empty()) {
            return {false, std::move(missing_args)};
        }
        return {true, std::nullopt};
    }

    std::any get_argument(const std::string& key) {
        auto it = arguments.find(key);
        if (it != arguments.end()) {
            return it->second;
        }
        return {};
    }

    void add_argument(
        const std::string& arg,
        bool required_flag = false,
        std::function<std::any(const std::string&)> arg_type =
            [](const std::string& v) -> std::any { return v; }
    ) {
        if (required_flag) {
            required.insert(arg);
        }
        types[arg] = std::move(arg_type);
    }

    std::any _convert_type(const std::string& arg, const std::string& value) {
        auto it = types.find(arg);
        if (it == types.end()) {
            return value;
        }
        try {
            return it->second(value);
        } catch (const std::invalid_argument&) {
            return value;
        } catch (const std::out_of_range&) {
            return value;
        }
    }
};