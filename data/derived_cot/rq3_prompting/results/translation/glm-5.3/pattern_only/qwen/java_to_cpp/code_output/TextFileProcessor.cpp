#include <cerrno>
#include <cstring>
#include <fstream>
#include <iterator>
#include <stdexcept>
#include <string>
#include <utility>

#include <nlohmann/json.hpp>

namespace org::example {

class TextFileProcessor {
private:
    std::string file_path;

public:
    explicit TextFileProcessor(std::string file_path)
        : file_path(std::move(file_path)) {}

    // Equivalent of Jackson's readValue(File, Object.class):
    // parses arbitrary JSON into a generic value (object/array/string/number/bool/null).
    // Throws on missing file or malformed JSON, like IOException in the Java version.
    nlohmann::json read_file_as_json() const {
        return nlohmann::json::parse(read_file());
    }

    // Equivalent of new String(Files.readAllBytes(...)): reads all raw bytes.
    std::string read_file() const {
        std::ifstream in(file_path, std::ios::in | std::ios::binary);
        if (!in) {
            throw std::runtime_error("Cannot open file '" + file_path +
                                     "': " + std::strerror(errno));
        }
        std::string content((std::istreambuf_iterator<char>(in)),
                            std::istreambuf_iterator<char>());
        if (in.bad()) {
            throw std::runtime_error("Failed reading file '" + file_path + "'");
        }
        return content;
    }

    // Equivalent of Files.write(..., content.getBytes()):
    // CREATE + TRUNCATE_EXISTING + WRITE of the raw bytes.
    void write_file(const std::string& content) const {
        std::ofstream out(file_path, std::ios::out | std::ios::binary | std::ios::trunc);
        if (!out) {
            throw std::runtime_error("Cannot open file '" + file_path +
                                     "': " + std::strerror(errno));
        }
        out.write(content.data(), static_cast<std::streamsize>(content.size()));
        out.flush();
        if (!out) {
            throw std::runtime_error("Failed writing to file '" + file_path + "'");
        }
    }

    // Equivalent of content.replaceAll("[^a-zA-Z]", "") applied byte-wise;
    // identical output for ASCII and for UTF-8 content (non-ASCII chars are dropped either way).
    std::string process_file() const {
        std::string content = read_file();
        std::string processedContent;
        processedContent.reserve(content.size());
        for (char c : content) {
            if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) {
                processedContent.push_back(c);
            }
        }
        write_file(processedContent);
        return processedContent;
    }
};

} // namespace org::example