// JSONProcessor.cpp — C++ translation of org.example.JSONProcessor
// Uses nlohmann/json (ordered_json preserves Gson's insertion-order map semantics).
// readJson returns std::nullopt to mirror Java's null return on missing file / parse error.

#include <cstdint>
#include <filesystem>
#include <fstream>
#include <optional>
#include <stdexcept>
#include <string>

#include "nlohmann/json.hpp"

namespace org::example {

namespace fs = std::filesystem;
using JsonObject = nlohmann::ordered_json;

class JSONProcessor {
public:
    // Java: Map<String, Object> readJson(String) -> null on missing file or any exception
    std::optional<JsonObject> readJson(const std::string& filePath) {
        std::error_code ec;
        if (!fs::exists(fs::path(filePath), ec)) {
            return std::nullopt;
        }
        try {
            std::ifstream reader(filePath);
            JsonObject parsed = JsonObject::parse(reader);
            // Gson's fromJson(reader, Map.class) fails on non-object JSON ("Expected BEGIN_OBJECT")
            if (!parsed.is_object()) {
                return std::nullopt;
            }
            toGsonNumberSemantics(parsed); // Gson maps all JSON numbers to Double in Object context
            return parsed;
        } catch (...) {
            return std::nullopt;
        }
    }

    // Java: boolean writeJson(Map<String, Object>, String) -> false on any exception
    bool writeJson(const JsonObject& data, const std::string& filePath) {
        try {
            std::ofstream writer(filePath, std::ios::out | std::ios::trunc); // FileWriter truncates
            if (!writer) {
                throw std::runtime_error("cannot open file for writing");
            }
            const std::string out = data.dump(); // compact form, like Gson's default
            writer << out;
            writer.flush();
            if (!writer) {
                throw std::runtime_error("write failed");
            }
            return true;
        } catch (...) {
            return false;
        }
    }

    // Java: boolean processJson(String, String)
    bool processJson(const std::string& filePath, const std::string& removeKey) {
        std::optional<JsonObject> data = readJson(filePath);
        if (!data) {
            return false;
        }
        if (data->contains(removeKey)) {
            data->erase(removeKey);
            return writeJson(*data, filePath);
        } else {
            return false;
        }
    }

private:
    // Gson deserializes every JSON number into Double when the target is Object,
    // so integers round-trip as "5.0". Convert integer nodes to doubles to match.
    static void toGsonNumberSemantics(JsonObject& node) {
        switch (node.type()) {
            case JsonObject::value_t::number_integer:
                node = static_cast<double>(node.get<std::int64_t>());
                break;
            case JsonObject::value_t::number_unsigned:
                node = static_cast<double>(node.get<std::uint64_t>());
                break;
            case JsonObject::value_t::object:
                for (auto& item : node.items()) {
                    toGsonNumberSemantics(item.value());
                }
                break;
            case JsonObject::value_t::array:
                for (auto& element : node) {
                    toGsonNumberSemantics(element);
                }
                break;
            default:
                break;
        }
    }
};

} // namespace org::example