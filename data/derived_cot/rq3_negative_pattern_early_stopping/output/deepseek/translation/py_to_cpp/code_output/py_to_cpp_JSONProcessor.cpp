#include <iostream>
#include <fstream>
#include <filesystem>
#include <variant>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

class JSONProcessor {
public:
    // Reads a JSON file and returns the parsed data.
    // Returns 0 if file does not exist.
    // Returns -1 if an error occurs during reading (e.g., malformed JSON).
    // Otherwise returns the JSON object.
    std::variant<int, json> read_json(const std::string& file_path) {
        if (!std::filesystem::exists(file_path)) {
            return 0;
        }
        try {
            std::ifstream file(file_path);
            if (!file.is_open()) {
                return -1;
            }
            json data;
            file >> data;
            return data;
        } catch (...) {
            return -1;
        }
    }

    // Writes the given JSON data to the specified file.
    // Returns 1 on success, -1 on failure.
    int write_json(const json& data, const std::string& file_path) {
        try {
            std::ofstream file(file_path);
            if (!file.is_open()) {
                return -1;
            }
            file << data.dump(4); // indented like Python's default
            return 1;
        } catch (...) {
            return -1;
        }
    }

    // Reads a JSON file, removes the specified key (if it exists),
    // and writes the modified data back.
    // Returns 1 if the key was removed and file was updated.
    // Returns 0 if the file does not exist, the key does not exist,
    //         or reading/writing fails (read returns 0 or -1).
    int process_json(const std::string& file_path, const std::string& remove_key) {
        auto result = read_json(file_path);
        // If read_json returned an int (0 or -1), treat as failure
        if (std::holds_alternative<int>(result)) {
            return 0;
        }
        json& data = std::get<json>(result);
        // If the JSON is not an object, the following will throw,
        // matching Python's TypeError when trying to index a non‑dict.
        if (data.contains(remove_key)) {
            data.erase(remove_key);
            write_json(data, file_path);
            return 1;
        }
        return 0;
    }
};