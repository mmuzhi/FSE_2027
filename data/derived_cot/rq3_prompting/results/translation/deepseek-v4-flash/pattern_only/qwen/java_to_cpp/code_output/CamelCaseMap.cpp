#include <any>
#include <cctype>
#include <functional>
#include <iterator>
#include <list>
#include <optional>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

class CamelCaseMap {
public:
    using Key = std::optional<std::string>;
    using Value = std::any;

    class KeySet {
    public:
        using iterator = std::list<Key>::const_iterator;
        using const_iterator = std::list<Key>::const_iterator;

        KeySet(CamelCaseMap& owner) : owner(owner) {}

        iterator begin() const { return owner.keys.cbegin(); }
        iterator end() const { return owner.keys.cend(); }
        int size() const { return static_cast<int>(owner.keys.size()); }
        bool empty() const { return owner.keys.empty(); }
        bool contains(const Key& key) const {
            return owner.data.find(owner.convertKey(key)) != owner.data.end();
        }
        bool erase(const Key& key) {
            Key converted = owner.convertKey(key);
            auto it = owner.data.find(converted);
            if (it == owner.data.end()) {
                return false;
            }
            owner.keys.erase(it->second.second);
            owner.data.erase(it);
            return true;
        }
        void clear() { owner.clear(); }

    private:
        CamelCaseMap& owner;
    };

    CamelCaseMap() = default;
    CamelCaseMap(const CamelCaseMap&) = delete;
    CamelCaseMap& operator=(const CamelCaseMap&) = delete;

    Value get(const Key& key) const {
        auto it = data.find(convertKey(key));
        if (it == data.end()) {
            return {};
        }
        return it->second.first;
    }

    void put(const Key& key, const Value& value) {
        Key converted = convertKey(key);
        auto it = data.find(converted);
        if (it != data.end()) {
            it->second.first = value;
        } else {
            keys.push_back(converted);
            auto listIt = std::prev(keys.end());
            data.emplace(converted, std::make_pair(value, listIt));
        }
    }

    void remove(const Key& key) {
        Key converted = convertKey(key);
        auto it = data.find(converted);
        if (it != data.end()) {
            keys.erase(it->second.second);
            data.erase(it);
        }
    }

    void clear() {
        keys.clear();
        data.clear();
    }

    KeySet keySet() { return KeySet(*this); }

    int size() const { return static_cast<int>(keys.size()); }

private:
    struct Hash {
        size_t operator()(const Key& k) const {
            if (!k.has_value()) {
                return 0;
            }
            return std::hash<std::string>{}(*k);
        }
    };

    std::list<Key> keys;
    std::unordered_map<Key, std::pair<Value, std::list<Key>::iterator>, Hash> data;

    Key convertKey(const Key& key) const {
        if (!key.has_value()) {
            return std::nullopt;
        }
        return toCamelCase(*key);
    }

    static Key toCamelCase(const std::string& key) {
        std::vector<std::string> parts;
        size_t start = 0;
        while (true) {
            size_t pos = key.find('_', start);
            if (pos == std::string::npos) {
                parts.push_back(key.substr(start));
                break;
            }
            parts.push_back(key.substr(start, pos - start));
            start = pos + 1;
        }
        while (!parts.empty() && parts.back().empty()) {
            parts.pop_back();
        }
        if (parts.empty()) {
            parts.push_back("");
        }

        std::string result = parts[0];
        for (size_t i = 1; i < parts.size(); ++i) {
            if (parts[i].empty()) {
                throw std::out_of_range("String index out of range: 0");
            }
            std::string first = parts[i].substr(0, 1);
            first[0] = static_cast<char>(std::toupper(static_cast<unsigned char>(first[0])));
            std::string rest = parts[i].substr(1);
            for (char& c : rest) {
                c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
            }
            result += first + rest;
        }
        return result;
    }
};