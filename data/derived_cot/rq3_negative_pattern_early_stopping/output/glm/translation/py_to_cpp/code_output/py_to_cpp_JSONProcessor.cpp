#include <fstream>
#include <filesystem>
#include <variant>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

class JSONProcessor {
public:
    std::variant<json, int> read_json(const std::string& file_path) {
        if (!std::filesystem::exists(file_path)) {
            return 0;
        }
        try {
            std::ifstream file(file_path);
            json data = json::parse(file);
            return data;
        } catch (...) {
            return -1;
        }
    }

    int write_json(const json& data, const std::string& file_path) {
        try {
            std::ofstream file(file_path);
            file << data.dump();
            return 1;
        } catch (...) {
            return -1;
        }
    }

    int process_json(const std::string& file_path, const std::string& remove_key) {
        auto result = read_json(file_path);
        if (std::holds_alternative<int>(result)) {
            int code = std::get<int>(result);
            if (code == 0 || code == -1) {
                return 0;
            }
        }
        json data = std::get<json>(result);
        if (data.contains(remove_key)) {
            data.erase(remove_key);
            write_json(data, file_path);
            return 1;
        } else {
            return 0;
        }
    }
};