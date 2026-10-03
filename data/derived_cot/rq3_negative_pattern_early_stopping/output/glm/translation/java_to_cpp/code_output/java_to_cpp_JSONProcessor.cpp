#pragma once

#include <filesystem>
#include <fstream>
#include <optional>
#include <string>
#include <nlohmann/json.hpp>

class JSONProcessor {
public:
    std::optional<nlohmann::json> readJson(const std::string& filePath) {
        if (!std::filesystem::exists(filePath)) {
            return std::nullopt;
        }
        try {
            std::ifstream file(filePath);
            if (!file.is_open()) {
                return std::nullopt;
            }
            nlohmann::json data = nlohmann::json::parse(file);
            if (!data.is_object()) {
                return std::nullopt;
            }
            return data;
        } catch (const std::exception&) {
            return std::nullopt;
        }
    }

    bool writeJson(const nlohmann::json& data, const std::string& filePath) {
        try {
            std::ofstream file(filePath);
            if (!file.is_open()) {
                return false;
            }
            file << data.dump();
            return true;
        } catch (const std::exception&) {
            return false;
        }
    }

    bool processJson(const std::string& filePath, const std::string& removeKey) {
        auto dataOpt = readJson(filePath);
        if (!dataOpt.has_value()) {
            return false;
        }
        nlohmann::json data = dataOpt.value();
        if (data.contains(removeKey)) {
            data.erase(removeKey);
            return writeJson(data, filePath);
        } else {
            return false;
        }
    }
};