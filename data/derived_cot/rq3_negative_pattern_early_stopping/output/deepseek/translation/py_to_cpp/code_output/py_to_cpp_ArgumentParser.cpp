#include <iostream>
#include <string>
#include <unordered_map>
#include <set>
#include <any>
#include <functional>
#include <sstream>
#include <optional>
#include <vector>
#include <stdexcept>

class ArgumentParser {
public:
    ArgumentParser() = default;

    // Add an argument specification.
    void add_argument(const std::string& arg, bool required = false, 
                      std::function<std::any(const std::string&)> arg_type = 
                          [](const std::string& s) -> std::any { return s; }) {
        if (required) {
            required_.insert(arg);
        }
        types_[arg] = std::move(arg_type);
    }

    // Parse a command line string (e.g. "python script.py --arg1=value1 -arg2 value2").
    // Returns: {true, nullopt} on success,
    //          {false, set of missing argument names} on failure.
    std::pair<bool, std::optional<std::set<std::string>>> 
    parse_arguments(const std::string& command_string) {
        // Split by whitespace and drop the first token (script name)
        std::istringstream iss(command_string);
        std::vector<std::string> tokens;
        std::string token;
        while (iss >> token) {
            tokens.push_back(token);
        }
        if (tokens.empty()) {
            // No command at all : treat as empty arguments
        } else {
            tokens.erase(tokens.begin()); // skip script name
        }

        arguments_.clear(); // reset

        for (size_t i = 0; i < tokens.size(); ++i) {
            const std::string& arg = tokens[i];

            if (arg.size() >= 2 && arg[0] == '-' && arg[1] == '-') {
                // --key=value or --key (flag)
                std::string key_value = arg.substr(2);
                auto eq_pos = key_value.find('=');
                if (eq_pos != std::string::npos) {
                    std::string key = key_value.substr(0, eq_pos);
                    std::string value = key_value.substr(eq_pos + 1);
                    arguments_[key] = convert_type(key, value);
                } else {
                    arguments_[key_value] = true; // flag
                }
            } else if (arg.size() >= 1 && arg[0] == '-') {
                // -key value or -key (flag)
                std::string key = arg.substr(1);
                if (i + 1 < tokens.size() && tokens[i+1][0] != '-') {
                    // next token is the value
                    arguments_[key] = convert_type(key, tokens[i+1]);
                    ++i; // consume the value token
                } else {
                    arguments_[key] = true; // flag
                }
            } else {
                // Ignore tokens that don't start with '-'
                // (the Python code only processes options)
            }
        }

        // Check for missing required arguments
        std::set<std::string> missing;
        for (const auto& req : required_) {
            if (arguments_.find(req) == arguments_.end()) {
                missing.insert(req);
            }
        }

        if (!missing.empty()) {
            return {false, std::move(missing)};
        }
        return {true, std::nullopt};
    }

    // Retrieve the value for a given argument.
    // Returns std::nullopt if the argument does not exist.
    std::optional<std::any> get_argument(const std::string& key) const {
        auto it = arguments_.find(key);
        if (it == arguments_.end()) {
            return std::nullopt;
        }
        return it->second;
    }

private:
    std::unordered_map<std::string, std::any> arguments_;
    std::set<std::string> required_;
    std::unordered_map<std::string, std::function<std::any(const std::string&)>> types_;

    // Try to convert the value according to the stored type function.
    // If conversion fails or the argument is not registered, return the original string.
    std::any convert_type(const std::string& arg, const std::string& value) {
        auto it = types_.find(arg);
        if (it == types_.end()) {
            return value; // no type registered -> keep as string
        }
        try {
            return it->second(value);
        } catch (const std::exception&) {
            return value; // conversion failed -> return original string
        }
    }
};