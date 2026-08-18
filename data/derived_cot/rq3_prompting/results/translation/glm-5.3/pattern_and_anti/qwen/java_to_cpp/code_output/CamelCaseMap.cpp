#pragma once

#include <any>
#include <cctype>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

class CamelCaseMap {
private:
    // Preserves LinkedHashMap semantics: iteration in insertion order,
    // re-put of an existing key updates in place without moving its position.
    std::vector<std::pair<std::string, std::any>> data;

    static std::vector<std::string> splitUnderscore(const std::string& key) {
        std::vector<std::string> parts;
        std::string cur;
        for (char c : key) {
            if (c == '_') {
                parts.push_back(cur);
                cur.clear();
            } else {
                cur += c;
            }
        }
        parts.push_back(cur);
        // Java's split("_") (limit 0) discards trailing empty parts.
        while (!parts.empty() && parts.back().empty()) {
            parts.pop_back();
        }
        // Java special case: "".split("_") yields [""]
        if (parts.empty() && key.empty()) {
            parts.emplace_back("");
        }
        return parts;
    }

public:
    std::any get(const std::string& key) {
        const std::string k = _convertKey(key);
        for (const auto& entry : data) {
            if (entry.first == k) {
                return entry.second;
            }
        }
        return std::any{}; // Java null
    }

    void put(const std::string& key, std::any value) {
        std::string k = _convertKey(key);
        for (auto& entry : data) {
            if (entry.first == k) {
                entry.second = std::move(value); // update in place, keep position
                return;
            }
        }
        data.emplace_back(std::move(k), std::move(value));
    }

    void remove(const std::string& key) {
        const std::string k = _convertKey(key);
        for (auto it = data.begin(); it != data.end(); ++it) {
            if (it->first == k) {
                data.erase(it);
                return;
            }
        }
    }

    std::string _convertKey(const std::string& key) {
        return _toCamelCase(key);
    }

    static std::string _toCamelCase(const std::string& key) {
        std::vector<std::string> parts = splitUnderscore(key);
        if (parts.empty()) {
            // Java: "_".split("_") -> [] -> parts[0] throws ArrayIndexOutOfBoundsException
            throw std::out_of_range("Array index out of range: 0");
        }
        std::string camelCaseString = parts[0];
        for (std::size_t i = 1; i < parts.size(); i++) {
            const std::string& p = parts[i];
            if (p.empty()) {
                // Java: "".substring(0, 1) throws StringIndexOutOfBoundsException
                throw std::out_of_range("String index out of range: 1");
            }
            // substring(0, 1).toUpperCase()
            camelCaseString += static_cast<char>(
                std::toupper(static_cast<unsigned char>(p[0])));
            // substring(1).toLowerCase()
            for (std::size_t j = 1; j < p.size(); j++) {
                camelCaseString += static_cast<char>(
                    std::tolower(static_cast<unsigned char>(p[j])));
            }
        }
        return camelCaseString;
    }

    std::vector<std::string> keySet() const {
        std::vector<std::string> keys;
        keys.reserve(data.size());
        for (const auto& entry : data) {
            keys.push_back(entry.first);
        }
        return keys;
    }

    int size() const {
        return static_cast<int>(data.size());
    }
};