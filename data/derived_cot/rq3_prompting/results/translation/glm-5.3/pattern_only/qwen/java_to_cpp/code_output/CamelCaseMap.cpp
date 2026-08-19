#include <any>
#include <cctype>
#include <cstddef>
#include <optional>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

class CamelCaseMap {
public:
    // Empty std::any plays the role of Java's null Object reference.
    using Object = std::any;

    CamelCaseMap() = default;

    std::any get(const std::optional<std::string>& key) {
        const std::optional<std::string> converted = _convertKey(key);
        for (const auto& entry : data) {
            if (entry.first == converted) {
                return entry.second;
            }
        }
        return std::any{}; // Java: returns null when key absent (or value is null)
    }
    std::any get(std::nullptr_t) { return get(std::optional<std::string>{}); }

    void put(const std::optional<std::string>& key, std::any value) {
        const std::optional<std::string> converted = _convertKey(key);
        for (auto& entry : data) {
            if (entry.first == converted) {
                entry.second = std::move(value); // LinkedHashMap: replace keeps original insertion position
                return;
            }
        }
        data.emplace_back(converted, std::move(value));
    }
    void put(std::nullptr_t, std::any value) { put(std::optional<std::string>{}, std::move(value)); }

    void remove(const std::optional<std::string>& key) {
        const std::optional<std::string> converted = _convertKey(key);
        for (auto it = data.begin(); it != data.end(); ++it) {
            if (it->first == converted) {
                data.erase(it);
                return;
            }
        }
    }
    void remove(std::nullptr_t) { remove(std::optional<std::string>{}); }

    std::optional<std::string> _convertKey(const std::optional<std::string>& key) const {
        if (!key.has_value()) {
            return std::nullopt;
        }
        return _toCamelCase(*key);
    }

    static std::string _toCamelCase(const std::string& key) {
        const std::vector<std::string> parts = splitOnUnderscore(key);
        if (parts.empty()) {
            // Java: "_".split("_") yields a zero-length array, so parts[0] throws
            throw std::out_of_range("Array index out of range: 0");
        }
        std::string camelCaseString = parts[0];
        for (std::size_t i = 1; i < parts.size(); ++i) {
            const std::string& part = parts[i];
            if (part.empty()) {
                // Java: "".substring(0, 1) throws StringIndexOutOfBoundsException
                // (interior empty parts, e.g. "a__b", are kept by split)
                throw std::out_of_range("String index out of range: 1");
            }
            camelCaseString.push_back(upperChar(part[0]));   // substring(0,1).toUpperCase()
            for (std::size_t j = 1; j < part.size(); ++j) {
                camelCaseString.push_back(lowerChar(part[j])); // substring(1).toLowerCase()
            }
        }
        return camelCaseString;
    }

    // Snapshot of keys in insertion order (Java returns a live Set view over the map).
    // std::nullopt entries correspond to Java's null key.
    std::vector<std::optional<std::string>> keySet() const {
        std::vector<std::optional<std::string>> keys;
        keys.reserve(data.size());
        for (const auto& entry : data) {
            keys.push_back(entry.first);
        }
        return keys;
    }

    int size() const {
        return static_cast<int>(data.size());
    }

private:
    // Insertion-ordered entries mirroring java.util.LinkedHashMap semantics:
    // replace keeps position, remove-then-put moves to the end, one null key allowed.
    std::vector<std::pair<std::optional<std::string>, std::any>> data;

    static std::vector<std::string> splitOnUnderscore(const std::string& key) {
        if (key.find('_') == std::string::npos) {
            // Java: no match -> single-element array containing the whole string
            // (important for the empty key: "".split("_") == [""])
            return {key};
        }
        std::vector<std::string> parts;
        std::string current;
        for (char c : key) {
            if (c == '_') {
                parts.push_back(current);
                current.clear();
            } else {
                current.push_back(c);
            }
        }
        parts.push_back(current);
        // Java split(regex, 0): all trailing empty strings removed (may yield empty array)
        while (!parts.empty() && parts.back().empty()) {
            parts.pop_back();
        }
        return parts;
    }

    static char upperChar(char c) {
        return static_cast<char>(std::toupper(static_cast<unsigned char>(c)));
    }

    static char lowerChar(char c) {
        return static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
    }
};