#include <string>
#include <fstream>
#include <sstream>
#include <cctype>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

class TextFileProcessor {
private:
    std::string file_path;

public:
    TextFileProcessor(std::string file_path) : file_path(std::move(file_path)) {}

    json read_file_as_json() {
        std::ifstream file(file_path);
        if (!file.is_open()) {
            throw std::ios_base::failure("File not found or cannot be opened: " + file_path);
        }
        
        json data;
        file >> data;
        return data;
    }

    std::string read_file() {
        std::ifstream file(file_path);
        if (!file.is_open()) {
            throw std::ios_base::failure("File not found or cannot be opened: " + file_path);
        }
        
        std::ostringstream ss;
        ss << file.rdbuf();
        return ss.str();
    }

    void write_file(const std::string& content) {
        std::ofstream file(file_path);
        if (!file.is_open()) {
            throw std::ios_base::failure("Cannot open file for writing: " + file_path);
        }
        
        file << content;
    }

    std::string process_file() {
        std::string content = read_file();
        std::string filtered;
        filtered.reserve(content.size());
        
        for (char c : content) {
            // Cast to unsigned char to avoid undefined behavior with std::isalpha
            if (std::isalpha(static_cast<unsigned char>(c))) {
                filtered += c;
            }
        }
        
        write_file(filtered);
        return filtered;
    }
};