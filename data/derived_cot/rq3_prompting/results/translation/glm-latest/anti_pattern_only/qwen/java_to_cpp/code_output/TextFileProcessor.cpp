#include <fstream>
#include <iterator>
#include <regex>
#include <stdexcept>
#include <string>
#include <utility>

// JSON support: nlohmann/json stands in for Jackson's ObjectMapper.
#include <nlohmann/json.hpp>

namespace org {
namespace example {

class TextFileProcessor {
public:
    explicit TextFileProcessor(std::string file_path)
        : file_path(std::move(file_path)) {}

    // Equivalent of objectMapper.readValue(new File(file_path), Object.class):
    // returns whatever JSON value the file contains (object, array, string,
    // number, boolean or null). Throws std::runtime_error if the file cannot
    // be opened, and nlohmann::json::parse_error on malformed JSON.
    nlohmann::json read_file_as_json() const {
        std::ifstream file(file_path, std::ios::binary);
        if (!file) {
            throw std::runtime_error("Cannot open file for reading: " + file_path);
        }
        return nlohmann::json::parse(file);
    }

    // Equivalent of new String(Files.readAllBytes(Paths.get(file_path))).
    std::string read_file() const {
        std::ifstream file(file_path, std::ios::binary);
        if (!file) {
            throw std::runtime_error("Cannot open file for reading: " + file_path);
        }
        return std::string(std::istreambuf_iterator<char>(file),
                           std::istreambuf_iterator<char>());
    }

    // Equivalent of Files.write(...): creates the file if absent,
    // otherwise truncates it, then writes the raw bytes.
    void write_file(const std::string& content) const {
        std::ofstream file(file_path, std::ios::binary | std::ios::trunc);
        if (!file) {
            throw std::runtime_error("Cannot open file for writing: " + file_path);
        }
        file.write(content.data(), static_cast<std::streamsize>(content.size()));
        if (!file) {
            throw std::runtime_error("Failed writing to file: " + file_path);
        }
    }

    std::string process_file() const {
        const std::string content = read_file();
        // content.replaceAll("[^a-zA-Z]", "")
        static const std::regex non_alpha("[^a-zA-Z]");
        const std::string processed_content =
            std::regex_replace(content, non_alpha, "");
        write_file(processed_content);
        return processed_content;
    }

private:
    std::string file_path;
};

}  // namespace example
}  // namespace org