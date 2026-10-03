#include <nlohmann/json.hpp>
#include <fstream>
#include <filesystem>
#include <iostream>

using json = nlohmann::json;

class JSONProcessor {
public:
    // Read a JSON file and return the data.
    // Returns 0 if the file does not exist, -1 if an error occurs, or the JSON object if successful.
    int read_json(const std::string& file_path) {
        // Check if the file exists
        if (!std::filesystem::exists(file_path)) {
            return 0;
        }

        try {
            std::ifstream input_file(file_path);
            if (!input_file.is_open()) {
                return -1;
            }
            json data = json::parse(input_file);
            return data;
        } catch (const std::exception& e) {
            return -1;
        } catch (...) {
            return -1;
        }
    }

    // Write data to a JSON file.
    // Returns 1 on success, -1 on error.
    int write_json(const json& data, const std::string& file_path) {
        try {
            std::ofstream output_file(file_path);
            if (!output_file.is_open()) {
                return -1;
            }
            output_file << data.dump(4); // Pretty print with indent 4
            return 1;
        } catch (...) {
            return -1;
        }
    }

    // Process JSON file by removing a specified key.
    // Returns 1 if key removed and written back, 0 otherwise (file not exists, key not found, or write error).
    int process_json(const std::string& file_path, const std::string& remove_key) {
        json data = read_json(file_path);
        // If read_json returns 0 or -1, then we return 0.
        if (data == 0 || data == -1) {
            return 0;
        }

        // Check if the key exists in the JSON object
        if (data.find(remove_key) != data.end()) {
            data.erase(remove_key);
            // Write the modified data back
            write_json(data, file_path);
            return 1;
        } else {
            return 0;
        }
    }
};