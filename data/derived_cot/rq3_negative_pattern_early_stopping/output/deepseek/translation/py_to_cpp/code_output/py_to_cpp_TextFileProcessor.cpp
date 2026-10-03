#include <fstream>
#include <string>
#include <sstream>
#include <algorithm>
#include <cctype>
#include <stdexcept>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

/**
 * The class handles reading, writing, and processing text files.
 * It can read the file as JSON, read the raw text, write content to the file,
 * and process the file by removing non-alphabetic characters.
 */
class TextFileProcessor {
private:
    std::string file_path;

public:
    /**
     * Initialize the file path.
     * @param file_path std::string
     */
    TextFileProcessor(const std::string& file_path) : file_path(file_path) {}

    /**
     * Read the file as JSON format.
     * If the file content doesn't obey JSON format, the code will raise an error.
     * @return json object (dict, list, string, number, etc.)
     *
     * Example:
     *   TextFileProcessor processor("test.json");
     *   json data = processor.read_file_as_json();
     *   // data == {"name": "test", "age": 12}
     */
    json read_file_as_json() {
        std::ifstream file(file_path);
        if (!file.is_open()) {
            throw std::runtime_error("Could not open file: " + file_path);
        }
        json data;
        file >> data;
        return data;
    }

    /**
     * Read the entire content of the file as a string.
     * @return std::string containing the file content
     *
     * Example:
     *   TextFileProcessor processor("test.json");
     *   std::string content = processor.read_file();
     *   // content == "{\n    \"name\": \"test\",\n    \"age\": 12\n}"
     */
    std::string read_file() {
        std::ifstream file(file_path);
        if (!file.is_open()) {
            throw std::runtime_error("Could not open file: " + file_path);
        }
        std::stringstream buffer;
        buffer << file.rdbuf();
        return buffer.str();
    }

    /**
     * Write content into the file, overwriting if the file already exists.
     * @param content std::string to write
     *
     * Example:
     *   TextFileProcessor processor("test.json");
     *   processor.write_file("Hello world!");
     *   std::string content = processor.read_file();
     *   // content == "Hello world!"
     */
    void write_file(const std::string& content) {
        std::ofstream file(file_path);
        if (!file.is_open()) {
            throw std::runtime_error("Could not open file for writing: " + file_path);
        }
        file << content;
    }

    /**
     * Read the file, filter out non-alphabetic characters from the content string,
     * overwrite the processed data into the same file, and return the processed string.
     * @return std::string containing only alphabetic characters
     *
     * Example:
     *   TextFileProcessor processor("test.json");
     *   std::string before = processor.read_file();
     *   // before == "{\n    \"name\": \"test\",\n    \"age\": 12\n}"
     *   std::string after = processor.process_file();
     *   // after == "nametestage"
     */
    std::string process_file() {
        std::string content = read_file();
        std::string processed;
        std::copy_if(content.begin(), content.end(), std::back_inserter(processed),
                     [](char c) { return std::isalpha(static_cast<unsigned char>(c)); });
        write_file(processed);
        return processed;
    }
};