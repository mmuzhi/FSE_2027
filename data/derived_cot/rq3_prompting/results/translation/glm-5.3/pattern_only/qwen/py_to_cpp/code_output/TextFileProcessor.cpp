#include <cctype>
#include <fstream>
#include <iterator>
#include <stdexcept>
#include <string>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

// Handles reading, writing, and processing text files: read as JSON,
// read raw text, write content, and filter non-alphabetic characters.
class TextFileProcessor {
public:
    std::string file_path;  // public attribute, mirrors Python

    // Initialize the file path.
    explicit TextFileProcessor(std::string filePath)
        : file_path(std::move(filePath)) {}

    // Read the file as JSON. Returns object/array/string/number/bool/null
    // depending on the content. Throws json::parse_error if the content
    // does not obey JSON format (like json.load raising an error).
    json read_file_as_json() const {
        const std::string content = read_file();
        return json::parse(content);
    }

    // Read and return the whole content of the file.
    // Throws std::runtime_error if the file cannot be opened
    // (like FileNotFoundError in Python).
    std::string read_file() const {
        std::ifstream file(file_path, std::ios::binary);
        if (!file) {
            throw std::runtime_error("[Errno 2] No such file or directory: '" + file_path + "'");
        }
        std::string content((std::istreambuf_iterator<char>(file)),
                            std::istreambuf_iterator<char>());

        // Python text mode 'r' uses universal newlines: \r\n and lone \r -> \n
        std::string normalized;
        normalized.reserve(content.size());
        for (std::size_t i = 0; i < content.size(); ++i) {
            if (content[i] == '\r') {
                normalized += '\n';
                if (i + 1 < content.size() && content[i + 1] == '\n') {
                    ++i;
                }
            } else {
                normalized += content[i];
            }
        }
        return normalized;
    }

    // Write content into the file, overwriting if it already exists.
    // Throws std::runtime_error if the file cannot be opened for writing
    // (like OSError in Python).
    void write_file(const std::string& content) const {
        std::ofstream file(file_path, std::ios::binary | std::ios::trunc);
        if (!file) {
            throw std::runtime_error("Unable to open file for writing: '" + file_path + "'");
        }
        file.write(content.data(), static_cast<std::streamsize>(content.size()));
        file.flush();
        if (!file) {
            throw std::runtime_error("Failed writing to file: '" + file_path + "'");
        }
    }

    // Read the file, filter out non-alphabetic characters, overwrite the
    // file with the processed data, and return the processed string.
    std::string process_file() {
        const std::string content = read_file();

        std::string filtered;
        filtered.reserve(content.size());
        for (char c : content) {
            // cast to unsigned char: std::isalpha with negative values is UB
            if (std::isalpha(static_cast<unsigned char>(c))) {
                filtered += c;
            }
        }

        write_file(filtered);
        return filtered;
    }
};