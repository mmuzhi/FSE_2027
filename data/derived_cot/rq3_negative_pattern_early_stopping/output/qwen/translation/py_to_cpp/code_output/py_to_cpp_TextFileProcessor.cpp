#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <stdexcept>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

class TextFileProcessor {
private:
    std::string file_path;

public:
    TextFileProcessor(const std::string& file_path) : file_path(file_path) {}

    // Read the file as JSON
    auto read_file_as_json() {
        std::ifstream file(file_path);
        if (!file.is_open()) {
            throw std::runtime_error("Failed to open file: " + file_path);
        }

        try {
            json j = json::parse(file);
            return j;
        } catch (const json::parse_error& e) {
            throw std::runtime_error("JSON parse error: " + std::string(e.what()));
        }
    }

    // Read the file as raw text
    std::string read_file() {
        std::ifstream file(file_path);
        if (!file.is_open()) {
            throw std::runtime_error("Failed to open file: " + file_path);
        }

        std::string content;
        std::string line;
        while (std::getline(file, line)) {
            content += line;
        }
        return content;
    }

    // Write content to the file
    void write_file(const std::string& content) {
        std::ofstream file(file_path);
        if (!file.is_open()) {
            throw std::runtime_error("Failed to open file: " + file_path);
        }

        file << content;
    }

    // Process the file: remove non-alphabetic characters and write back
    std::string process_file() {
        std::string content = read_file();
        // Remove non-alphabetic characters
        content.erase(std::remove_if(content.begin(), content.end(), [](unsigned char c) {
            return !isalpha(c);
        }), content.end());

        write_file(content);
        return content;
    }
};