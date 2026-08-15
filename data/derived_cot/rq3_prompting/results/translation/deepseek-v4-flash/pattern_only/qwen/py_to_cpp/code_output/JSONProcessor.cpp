#include <nlohmann/json.hpp>
#include <filesystem>
#include <fstream>
#include <sstream>
#include <string>
#include <stdexcept>
#include <system_error>

class JSONProcessor {
public:
    nlohmann::ordered_json read_json(const std::string& file_path);
    int write_json(const nlohmann::ordered_json& data, const std::string& file_path);
    int process_json(const std::string& file_path, const std::string& remove_key);
};

static bool python_eq_zero(const nlohmann::ordered_json& j) {
    if (j.is_boolean()) {
        return j.get<bool>() == false;
    }
    if (j.is_number()) {
        return j.get<double>() == 0.0;
    }
    return false;
}

static bool python_eq_neg_one(const nlohmann::ordered_json& j) {
    if (j.is_boolean()) {
        return false;
    }
    if (j.is_number()) {
        return j.get<double>() == -1.0;
    }
    return false;
}

static bool python_in(const std::string& key, const nlohmann::ordered_json& data) {
    if (data.is_object()) {
        return data.contains(key);
    }
    if (data.is_array()) {
        for (const auto& element : data) {
            if (element == nlohmann::ordered_json(key)) {
                return true;
            }
        }
        return false;
    }
    if (data.is_string()) {
        return data.get<std::string>().find(key) != std::string::npos;
    }
    throw std::runtime_error("argument of type '" + data.type_name() + "' is not iterable");
}

static std::string python_json_dump(const nlohmann::ordered_json& j) {
    if (j.is_object()) {
        std::string result = "{";
        bool first = true;
        for (auto it = j.begin(); it != j.end(); ++it) {
            if (!first) result += ", ";
            first = false;
            result += nlohmann::ordered_json(it.key()).dump(-1, ' ', true);
            result += ": ";
            result += python_json_dump(it.value());
        }
        result += "}";
        return result;
    }
    if (j.is_array()) {
        std::string result = "[";
        bool first = true;
        for (const auto& element : j) {
            if (!first) result += ", ";
            first = false;
            result += python_json_dump(element);
        }
        result += "]";
        return result;
    }
    return j.dump(-1, ' ', true);
}

nlohmann::ordered_json JSONProcessor::read_json(const std::string& file_path) {
    std::error_code ec;
    std::filesystem::path path(file_path);
    bool exists = std::filesystem::exists(path, ec);
    if (ec) {
        exists = false;
    }
    if (!exists) {
        return nlohmann::ordered_json(0);
    }
    try {
        std::ifstream file(path);
        if (!file.is_open()) {
            return nlohmann::ordered_json(-1);
        }
        std::stringstream buffer;
        buffer << file.rdbuf();
        std::string content = buffer.str();
        nlohmann::ordered_json data = nlohmann::ordered_json::parse(content);
        return data;
    } catch (...) {
        return nlohmann::ordered_json(-1);
    }
}

int JSONProcessor::write_json(const nlohmann::ordered_json& data, const std::string& file_path) {
    try {
        std::ofstream file;
        file.exceptions(std::ofstream::failbit | std::ofstream::badbit);
        file.open(std::filesystem::path(file_path));
        std::string content = python_json_dump(data);
        file << content;
        return 1;
    } catch (...) {
        return -1;
    }
}

int JSONProcessor::process_json(const std::string& file_path, const std::string& remove_key) {
    nlohmann::ordered_json data = read_json(file_path);
    if (python_eq_zero(data) || python_eq_neg_one(data)) {
        return 0;
    }
    if (python_in(remove_key, data)) {
        data.erase(remove_key);
        write_json(data, file_path);
        return 1;
    } else {
        return 0;
    }
}