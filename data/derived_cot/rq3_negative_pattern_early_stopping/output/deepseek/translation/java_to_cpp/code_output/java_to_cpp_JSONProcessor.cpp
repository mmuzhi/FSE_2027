#include <nlohmann/json.hpp>
#include <fstream>
#include <filesystem>
#include <optional>
#include <map>
#include <string>

using json = nlohmann::json;

std::optional<json> readJson(const std::string& filePath) {
    if (!std::filesystem::exists(filePath)) {
        return std::nullopt;
    }
    std::ifstream ifs(filePath);
    if (!ifs.is_open()) {
        return std::nullopt;
    }
    try {
        json j;
        ifs >> j;
        return j;
    } catch (const std::exception&) {
        return std::nullopt;
    }
}

bool writeJson(const json& data, const std::string& filePath) {
    std::ofstream ofs(filePath);
    if (!ofs.is_open()) {
        return false;
    }
    try {
        ofs << data.dump(2);
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
    json& data = dataOpt.value();
    if (!data.is_object()) {
        return false;
    }
    if (data.contains(removeKey)) {
        data.erase(removeKey);
        return writeJson(data, filePath);
    } else {
        return false;
    }
}