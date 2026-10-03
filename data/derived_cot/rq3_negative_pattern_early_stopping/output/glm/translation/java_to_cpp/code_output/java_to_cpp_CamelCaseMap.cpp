#include <string>
#include <any>
#include <vector>
#include <unordered_map>
#include <list>
#include <cctype>
#include <optional>
#include <stdexcept>

struct OptionalStringHash {
    std::size_t operator()(const std::optional<std::string>& opt) const {
        if (!opt.has_value()) return 0;
        return std::hash<std::string>{}(*opt);
    }
};

class CamelCaseMap {
private:
    using ListType = std::list<std::pair<std::optional<std::string>, std::any>>;
    ListType order;
    std::unordered_map<std::optional<std::string>, ListType::iterator, OptionalStringHash> data;

    static std::vector<std::string> split_underscore(const std::string& key) {
        std::vector<std::string> parts;
        std::string current;
        for (char c : key) {
            if (c == '_') {
                parts.push_back(current);
                current.clear();
            } else {
                current += c;
            }
        }
        parts.push_back(current);
        while (!parts.empty() && parts.back().empty()) {
            parts.pop_back();
        }
        return parts;
    }

public:
    std::any get(const std::optional<std::string>& key) {
        auto ckey = _convertKey(key);
        auto it = data.find(ckey);
        if (it != data.end()) {
            return it->second->second;
        }
        return std::any();
    }

    void put(const std::optional<std::string>& key, std::any value) {
        auto ckey = _convertKey(key);
        auto it = data.find(ckey);
        if (it != data.end()) {
            it->second->second = std::move(value);
        } else {
            order.emplace_back(ckey, std::move(value));
            data[ckey] = std::prev(order.end());
        }
    }

    void remove(const std::optional<std::string>& key) {
        auto ckey = _convertKey(key);
        auto it = data.find(ckey);
        if (it != data.end()) {
            order.erase(it->second);
            data.erase(it);
        }
    }

    std::optional<std::string> _convertKey(const std::optional<std::string>& key) const {
        if (!key.has_value()) {
            return std::nullopt;
        }
        return _toCamelCase(key.value());
    }

    static std::string _toCamelCase(const std::string& key) {
        std::vector<std::string> parts = split_underscore(key);
        if (parts.empty()) {
            throw std::out_of_range("key results in empty parts");
        }

        std::string camelCaseString = parts[0];
        for (size_t i = 1; i < parts.size(); i++) {
            if (parts[i].empty()) {
                throw std::out_of_range("Empty part between underscores");
            }
            camelCaseString += static_cast<char>(std::toupper(static_cast<unsigned char>(parts[i][0])));
            for (size_t j = 1; j < parts[i].length(); j++) {
                camelCaseString += static_cast<char>(std::tolower(static_cast<unsigned char>(parts[i][j])));
            }
        }
        return camelCaseString;
    }

    std::vector<std::optional<std::string>> keySet() const {
        std::vector<std::optional<std::string>> keys;
        for (const auto& pair : order) {
            keys.push_back(pair.first);
        }
        return keys;
    }

    int size() const {
        return data.size();
    }
};