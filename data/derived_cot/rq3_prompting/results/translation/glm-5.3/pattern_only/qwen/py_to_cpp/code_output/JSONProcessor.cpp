#include <fstream>
#include <filesystem>
#include <string>
#include "nlohmann/json.hpp"

using json = nlohmann::json;
namespace fs = std::filesystem;

// Class to process JSON files: reading, writing, and removing a specified key.
class JSONProcessor {
public:
    // Returns the parsed data on success, 0 if the file does not exist,
    // or -1 if an error occurs during the reading process.
    json read_json(const std::string& file_path) {
        if (!fs::exists(file_path)) {
            return 0;
        }
        try {
            std::ifstream file(file_path);
            json data;
            file >> data;  // throws on parse/open failure
            return data;
        } catch (...) {
            return -1;
        }
    }

    // Returns 1 if the writing process is successful, or -1 if an error occurs.
    int write_json(const json& data, const std::string& file_path) {
        try {
            std::ofstream file(file_path);  // truncates like 'w' mode
            if (!file.is_open()) {
                return -1;
            }
            file << data.dump();
            return 1;
        } catch (...) {
            return -1;
        }
    }

    // Reads a JSON file, removes the specified key, and rewrites the file.
    // Returns 1 on success, 0 if the file or key does not exist (or read failed).
    int process_json(const std::string& file_path, const std::string& remove_key) {
        json data = read_json(file_path);
        if (data == 0 || data == -1) {
            return 0;
        }
        if (data.contains(remove_key)) {
            data.erase(remove_key);
            write_json(data, file_path);
            return 1;
        } else {
            return 0;
        }
    }
};