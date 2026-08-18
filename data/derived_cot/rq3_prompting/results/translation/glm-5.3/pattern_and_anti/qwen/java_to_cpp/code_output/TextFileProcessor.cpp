#include <fstream>
#include <sstream>
#include <stdexcept>
#include <string>

#include <nlohmann/json.hpp>

class TextFileProcessor {
private:
    std::string file_path;

public:
    explicit TextFileProcessor(const std::string& file_path)
        : file_path(file_path) {}

    // Java: Jackson readValue into Object -> generic JSON value (throws on malformed input, like Jackson)
    nlohmann::json read_file_as_json() const {
        return nlohmann::json::parse(read_file());
    }

    // Java: new String(Files.readAllBytes(...)) -> raw byte-preserving read
    std::string read_file() const {
        std::ifstream in(file_path, std::ios::binary);
        if (!in) {
            throw std::runtime_error("IOException: cannot open file for reading: " + file_path);
        }
        std::ostringstream ss;
        ss << in.rdbuf();
        if (!in && !in.eof()) {
            throw std::runtime_error("IOException: failed reading file: " + file_path);
        }
        return ss.str();
    }

    // Java: Files.write with default options (CREATE, TRUNCATE_EXISTING, WRITE)
    void write_file(const std::string& content) const {
        std::ofstream out(file_path, std::ios::binary | std::ios::trunc);
        if (!out) {
            throw std::runtime_error("IOException: cannot open file for writing: " + file_path);
        }
        out << content;
        out.flush();
        if (!out) {
            throw std::runtime_error("IOException: failed writing file: " + file_path);
        }
    }

    // Java: replaceAll("[^a-zA-Z]", "") -> keep only ASCII letters
    // Byte-wise filtering matches Java's char-wise result for UTF-8 input:
    // all non-ASCII bytes (>= 0x80) are dropped either way.
    std::string process_file() {
        std::string content = read_file();
        std::string processedContent;
        processedContent.reserve(content.size());
        for (unsigned char c : content) {
            if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) {
                processedContent += static_cast<char>(c);
            }
        }
        write_file(processedContent);
        return processedContent;
    }
};