#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <stdexcept>
#include <memory>
#include <typeinfo>
#include <cxxabi.h> // maybe not needed

// Simulate Java's Class<?> with enum
enum class ArgType { INT, BOOL, STRING, UNKNOWN };

// Simple tuple struct
template<typename X, typename Y>
struct Tuple {
    X x;
    Y y;
    Tuple(X x, Y y) : x(x), y(y) {}
};

class ArgumentParser {
private:
    std::unordered_map<std::string, std::string> arguments; // key -> value stored as string? Java stores Object. We'll store string and convert on get? Or use variant. Simpler: store string representation and convert when needed. But for consistency, we need to return Object. In C++ we can store std::any or boost::any. But for simplicity and to match behavior, we'll store as std::string but keep conversion inside parseArguments. Actually Java stores the converted value in arguments map. So we need to store the converted value. Use std::any.
    std::unordered_map<std::string, std::any> arguments;
    std::unordered_set<std::string> required;
    std::unordered_map<std::string, ArgType> types;

    std::any convertType(const std::string& arg, const std::string& value) {
        auto it = types.find(arg);
        if (it == types.end()) return value; // unknown type, return string
        try {
            switch (it->second) {
                case ArgType::INT:
                    return std::stoi(value);
                case ArgType::BOOL:
                    // Java's Boolean.parseBoolean: true if "true" (case insensitive?)
                    // Actually Java's Boolean.parseBoolean: "true" (case insensitive) -> true; else false.
                    // We'll do the same.
                    {
                        std::string lower = value;
                        for (auto& c : lower) c = std::tolower(c);
                        return lower == "true";
                    }
                case ArgType::STRING:
                    return value;
                default:
                    return value;
            }
        } catch (const std::exception&) {
            return value; // on error return original string
        }
    }

public:
    ArgumentParser() {}

    Tuple<bool, std::unordered_set<std::string>> parseArguments(const std::string& commandString) {
        // Split by whitespace
        std::vector<std::string> args;
        std::istringstream iss(commandString);
        std::string token;
        while (iss >> token) {
            args.push_back(token);
        }
        for (size_t i = 1; i < args.size(); ++i) {
            const std::string& arg = args[i];
            if (arg.size() >= 2 && arg[0] == '-' && arg[1] == '-') {
                // long option
                std::string keyValue = arg.substr(2);
                size_t eqPos = keyValue.find('=');
                if (eqPos != std::string::npos) {
                    std::string key = keyValue.substr(0, eqPos);
                    std::string value = keyValue.substr(eqPos + 1);
                    arguments[key] = convertType(key, value);
                } else {
                    arguments[keyValue] = true; // boolean true
                }
            } else if (arg.size() >= 2 && arg[0] == '-' && arg[1] != '-') {
                // short option
                std::string key = arg.substr(1);
                if (i + 1 < args.size() && args[i+1][0] != '-') {
                    arguments[key] = convertType(key, args[i+1]);
                    ++i;
                } else {
                    arguments[key] = true;
                }
            }
        }
        std::unordered_set<std::string> missingArgs = required;
        for (auto& kv : arguments) {
            missingArgs.erase(kv.first);
        }
        if (!missingArgs.empty()) {
            return Tuple<bool, std::unordered_set<std::string>>(false, missingArgs);
        }
        return Tuple<bool, std::unordered_set<std::string>>(true, std::unordered_set<std::string>());
    }

    std::any getArgument(const std::string& key) {
        auto it = arguments.find(key);
        if (it != arguments.end()) return it->second;
        return std::any();
    }

    void addArgument(const std::string& arg, bool required, ArgType argType) {
        if (required) this->required.insert(arg);
        types[arg] = argType;
    }

    // For demonstration: print arguments as Java's map print
    void printArguments() {
        std::cout << "{";
        bool first = true;
        for (const auto& kv : arguments) {
            if (!first) std::cout << ", ";
            first = false;
            std::cout << kv.first << "=";
            // Print the any value
            if (kv.second.type() == typeid(int)) {
                std::cout << std::any_cast<int>(kv.second);
            } else if (kv.second.type() == typeid(bool)) {
                std::cout << (std::any_cast<bool>(kv.second) ? "true" : "false");
            } else if (kv.second.type() == typeid(std::string)) {
                std::cout << std::any_cast<std::string>(kv.second);
            } else {
                std::cout << "?";
            }
        }
        std::cout << "}" << std::endl;
    }
};

int main() {
    ArgumentParser parser;
    parser.addArgument("arg1", true, ArgType::INT);
    parser.addArgument("arg2", false, ArgType::STRING);
    parser.addArgument("option1", false, ArgType::BOOL);
    parser.addArgument("option2", false, ArgType::BOOL);

    Tuple<bool, std::unordered_set<std::string>> result = parser.parseArguments("python script.py --arg1=123 -arg2 value2 --option1 -option2");
    std::cout << (result.x ? "true" : "false") << std::endl;
    if (!result.y.empty()) {
        std::cout << "{";
        bool first = true;
        for (const auto& s : result.y) {
            if (!first) std::cout << ", ";
            first = false;
            std::cout << s;
        }
        std::cout << "}" << std::endl;
    } else {
        std::cout << "null" << std::endl;
    }
    parser.printArguments();
    return 0;
}