#include <iostream>
#include <string>
#include <unordered_map>
#include <set>
#include <vector>
#include <sstream>
#include <functional>
#include <any>

class ArgumentParser {
private:
    std::unordered_map<std::string, std::any> arguments_;
    std::set<std::string> required_;
    std::unordered_map<std::string, std::function<std::any(const std::string&)>> types_;

    std::any _convert_type(const std::string& arg, const std::string& value) {
        try {
            return types_[arg](value);
        } catch (...) {
            return value;
        }
    }

public:
    ArgumentParser() = default;

    bool parse_arguments(const std::string& command_string) {
        std::istringstream iss(command_string);
        std::vector<std::string> tokens;
        std::string token;
        while (iss >> token) {
            tokens.push_back(token);
        }

        if (!tokens.empty()) {
            tokens.erase(tokens.begin());
        }

        for (size_t i = 0; i < tokens.size(); ++i) {
            const std::string& arg_str = tokens[i];
            if (arg_str.starts_with("--")) {
                std::string key_value = arg_str.substr(2);
                auto pos = key_value.find('=');
                if (pos != std::string::npos) {
                    std::string key = key_value.substr(0, pos);
                    std::string value = key_value.substr(pos + 1);
                    arguments_[key] = _convert_type(key, value);
                } else {
                    arguments_[arg_str.substr(2)] = true;
                }
            } else if (arg_str.starts_with("-")) {
                std::string key = arg_str.substr(1);
                if (i + 1 < tokens.size() && !tokens[i + 1].starts_with('-')) {
                    arguments_[key] = _convert_type(key, tokens[i + 1]);
                } else {
                    arguments_[key] = true;
                }
            }
        }

        std::set<std::string> missing_args;
        for (const auto& req : required_) {
            if (arguments_.find(req) == arguments_.end()) {
                missing_args.insert(req);
            }
        }

        if (!missing_args.empty()) {
            return false;
        }

        return true;
    }

    std::any get_argument(const std::string& key) {
        auto it = arguments_.find(key);
        if (it != arguments_.end()) {
            return it->second;
        }
        return std::any();
    }

    void add_argument(const std::string& arg, bool required = false, std::function<std::any(const std::string&)> conversion = [](const std::string& s) { return s; }) {
        if (required) {
            required_.insert(arg);
        }
        types_[arg] = conversion;
    }
};