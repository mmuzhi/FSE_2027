#include <cctype>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>

#include <nlohmann/json.hpp>

class TextFileProcessor {
public:
    // Public to mirror the accessible Python attribute `self.file_path`.
    std::string file_path;

    explicit TextFileProcessor(std::string filePath)
        : file_path(std::move(filePath)) {}

    // Read the file as JSON.
    // Throws nlohmann::json::parse_error if the content does not obey the
    // JSON format (the analogue of Python's json.JSONDecodeError), and
    // std::runtime_error if the file cannot be opened (the analogue of
    // Python's FileNotFoundError).
    nlohmann::json read_file_as_json() const {
        std::ifstream file(file_path);
        if (!file) {
            throw std::runtime_error(
                "[Errno 2] No such file or directory: '" + file_path + "'");
        }
        return nlohmann::json::parse(file);
    }

    // Read and return the whole content of the file.
    // Throws std::runtime_error if the file cannot be opened.
    std::string read_file() const {
        std::ifstream file(file_path);
        if (!file) {
            throw std::runtime_error(
                "[Errno 2] No such file or directory: '" + file_path + "'");
        }
        std::ostringstream buffer;
        buffer << file.rdbuf();
        return buffer.str();
    }

    // Write content into the file, overwriting it if it already exists.
    // Throws std::runtime_error if the file cannot be opened for writing.
    void write_file(const std::string& content) {
        std::ofstream file(file_path, std::ios::out | std::ios::trunc);
        if (!file) {
            throw std::runtime_error(
                "Unable to open file for writing: '" + file_path + "'");
        }
        file << content;
    }

    // Read the file, keep only alphabetic characters, overwrite the file
    // with the filtered content, and return the processed string.
    std::string process_file() {
        std::string content = read_file();

        std::string processed;
        for (char c : content) {
            if (std::isalpha(static_cast<unsigned char>(c))) {
                processed += c;
            }
        }

        write_file(processed);
        return processed;
    }
};