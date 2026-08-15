#include <nlohmann/json.hpp>
#include <filesystem>
#include <fstream>
#include <optional>
#include <string>

class JSONProcessor {
public:
    std::optional<nlohmann::ordered_json> readJson(const std::string& filePath) {
        try {
            if (!std::filesystem::exists(filePath)) {
                return std::nullopt;
            }

            std::ifstream reader(filePath);
            if (!reader.is_open()) {
                return std::nullopt;
            }

            nlohmann::ordered_json parsed = nlohmann::ordered_json::parse(reader);
            if (!parsed.is_object()) {
                return std::nullopt;
            }

            return parsed;
        } catch (...) {
            return std::nullopt;
        }
    }

    bool writeJson(const nlohmann::ordered_json& data, const std::string& filePath) {
        try {
            std::ofstream writer(filePath);
            if (!writer.is_open()) {
                return false;
            }

            writer.exceptions(std::ofstream::failbit | std::ofstream::badbit);
            writer << data.dump();
            writer.flush();
            writer.close();

            return true;
        } catch (...) {
            return false;
        }
    }

    bool processJson(const std::string& filePath, const std::string& removeKey) {
        auto data = readJson(filePath);
        if (!data) {
            return false;
        }

        if (!data->contains(removeKey)) {
            return false;
        }

        data->erase(removeKey);
        return writeJson(*data, filePath);
    }
};