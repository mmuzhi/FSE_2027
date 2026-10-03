#include <fstream>
#include <nlohmann/json.hpp>
#include <string>

using json = nlohmann::json;

class JSONProcessor {
public:
    // Read JSON from file
    json readJson(const std::string& filePath) {
        try {
            std::ifstream file(filePath);
            if (!file) {
                return nullptr;
            }
            return json::parse(file);
        } catch (...) {
            return nullptr;
        }
    }

    // Write JSON to file
    bool writeJson(const json& data, const std::string& filePath) {
        try {
            std::ofstream file(filePath);
            if (!file) {
                return false;
            }
            file << data;
            return true;
        } catch (...) {
            return false;
        }
    }

    // Process the JSON: remove the key and write back
    bool processJson(const std::string& filePath, const std::string& removeKey) {
        json data = readJson(filePath);
        if (data == nullptr) {
            return false;
        }
        if (data.find(removeKey) != data.end()) {
            data.erase(removeKey);
            return writeJson(data, filePath);
        }
        return false;
    }
};