#include <filesystem>
#include <fstream>
#include <optional>
#include <string>

#include <nlohmann/json.hpp>

// Stable mapping:
//   Map<String, Object>  -> nlohmann::ordered_json (object; preserves insertion order like Gson's LinkedTreeMap)
//   null return          -> std::optional without a value
//   Gson number policy   -> numbers become double (Gson deserializes into Double for Object targets)
class JSONProcessor {
public:
    using JsonObject = nlohmann::ordered_json;

    std::optional<JsonObject> readJson(const std::string& filePath) {
        std::error_code ec;
        if (!std::filesystem::exists(std::filesystem::path(filePath), ec)) {
            return std::nullopt;
        }
        try {
            std::ifstream reader(filePath, std::ios::binary);
            if (!reader) {
                return std::nullopt;
            }
            JsonObject data = JsonObject::parse(reader);
            if (!data.is_object()) {
                // Gson cannot bind a non-object document to Map.class -> exception -> null
                return std::nullopt;
            }
            normalizeNumbers(data);
            return data;
        } catch (const std::exception&) {
            return std::nullopt;
        }
    }

    bool writeJson(const JsonObject& data, const std::string& filePath) {
        try {
            std::ofstream writer(filePath, std::ios::binary | std::ios::trunc);
            if (!writer) {
                return false;
            }
            writer << data.dump();
            writer.flush();
            return writer.good();
        } catch (const std::exception&) {
            return false;
        }
    }

    bool processJson(const std::string& filePath, const std::string& removeKey) {
        std::optional<JsonObject> data = readJson(filePath);
        if (!data.has_value()) {
            return false;
        }
        auto it = data->find(removeKey);
        if (it != data->end()) {
            data->erase(it);
            return writeJson(*data, filePath);
        }
        return false;
    }

private:
    static void normalizeNumbers(JsonObject& node) {
        switch (node.type()) {
            case JsonObject::value_t::number_integer:
            case JsonObject::value_t::number_unsigned:
                node = node.get<double>();
                break;
            case JsonObject::value_t::object:
                for (auto& kv : node.items()) {
                    normalizeNumbers(kv.value());
                }
                break;
            case JsonObject::value_t::array:
                for (auto& element : node) {
                    normalizeNumbers(element);
                }
                break;
            default:
                break;
        }
    }
};