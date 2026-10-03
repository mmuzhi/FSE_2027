#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <regex>
#include <filesystem>
#include <stdexcept>
#include <nlohmann/json.hpp>  // Requires nlohmann/json library

using json = nlohmann::json;

class TextFileProcessor {
private:
    std::string file_path;

public:
    // Constructor
    TextFileProcessor(const std::string& file_path) : file_path(file_path) {}

    // Reads file, parses as JSON, and returns the parsed object
    json read_file_as_json() {
        try {
            std::string content = read_file();
            return json::parse(content);
        } catch (const std::exception& e) {
            throw std::runtime_error("Failed to read or parse JSON file: " + std::string(e.what()));
        }
    }

    // Reads entire file content as a string
    std::string read_file() {
        try {
            // Get file size
            std::uintmax_t size = std::filesystem::file_size(file_path);
            std::ifstream file(file_path, std::ios::binary);
            if (!file) {
                throw std::runtime_error("Failed to open file: " + file_path);
            }
            std::string content(size, '\0');
            file.read(content.data(), size);
            if (!file) {
                throw std::runtime_error("Failed to read whole file: " + file_path);
            }
            return content;
        } catch (const std::exception& e) {
            throw std::runtime_error("File read error: " + std::string(e.what()));
        }
    }

    // Writes content to file (overwrites)
    void write_file(const std::string& content) {
        try {
            std::ofstream file(file_path, std::ios::binary | std::ios::trunc);
            if (!file) {
                throw std::runtime_error("Failed to open file for writing: " + file_path);
            }
            file.write(content.data(), content.size());
            if (!file) {
                throw std::runtime_error("Failed to write file: " + file_path);
            }
        } catch (const std::exception& e) {
            throw std::runtime_error("File write error: " + std::string(e.what()));
        }
    }

    // Reads file, removes all non‑alphabetic characters, writes back, returns processed content
    std::string process_file() {
        std::string content = read_file();
        std::regex non_alpha("[^a-zA-Z]");
        std::string processed = std::regex_replace(content, non_alpha, "");
        write_file(processed);
        return processed;
    }
};