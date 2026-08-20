#include <filesystem>
#include <fstream>
#include <optional>
#include <string>
#include <system_error>

#include <nlohmann/json.hpp>  // requires the nlohmann/json single header (Gson equivalent)

namespace org::example {

// Java's Map<String, Object> produced by Gson's fromJson(reader, Map.class) is a
// LinkedTreeMap: JSON objects only, insertion-ordered, nullable.
// nlohmann::ordered_json + std::optional reproduces those semantics.
using JsonMap = nlohmann::ordered_json;

class JSONProcessor {
public:
    // Java: public Map<String, Object> readJson(String filePath)
    std::optional<JsonMap> readJson(const std::string& filePath) {
        std::error_code ec;
        if (!std::filesystem::exists(filePath, ec)) {
            return std::nullopt;  // file does not exist (or existence undeterminable)
        }
        try {
            std::ifstream reader(filePath);
            if (!reader.is_open()) {
                return std::nullopt;  // like FileReader's FileNotFoundException -> null
            }
            JsonMap data = JsonMap::parse(reader);
            // Gson with Map.class only yields a Map for a top-level JSON object;
            // empty input, "null", arrays and scalars all end up as null in Java.
            if (!data.is_object()) {
                return std::nullopt;
            }
            return data;
        } catch (...) {
            return std::nullopt;  // Java: catch (Exception e) { return null; }
        }
    }

    // Java: public boolean writeJson(Map<String, Object> data, String filePath)
    bool writeJson(const JsonMap& data, const std::string& filePath) {
        try {
            std::ofstream writer(filePath);
            if (!writer.is_open()) {
                return false;  // like FileWriter's IOException -> false
            }
            writer << data.dump();  // Gson's default output is compact JSON
            writer.close();         // mirrors try-with-resources close();
            return !writer.fail();  // a failed write/flush/close -> false
        } catch (...) {
            return false;  // Java: catch (Exception e) { return false; }
        }
    }

    // Java: public boolean processJson(String filePath, String removeKey)
    bool processJson(const std::string& filePath, const std::string& removeKey) {
        std::optional<JsonMap> data = readJson(filePath);
        if (!data.has_value()) {
            return false;
        }
        if (data->contains(removeKey)) {
            data->erase(removeKey);
            return writeJson(*data, filePath);
        }
        return false;
    }
};

}  // namespace org::example