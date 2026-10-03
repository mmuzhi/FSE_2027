#include <any>
#include <cctype>
#include <list>
#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

class CamelCaseMap {
public:
    // Key type used internally (nullopt represents Java null)
    using Key = std::optional<std::string>;

    CamelCaseMap() = default;
    ~CamelCaseMap() = default;
    CamelCaseMap(const CamelCaseMap&) = delete;
    CamelCaseMap& operator=(const CamelCaseMap&) = delete;

    // get (nullptr allowed – represents Java null key)
    std::any get(const std::string* key) const {
        Key k = convertKey(key);
        return getImpl(k);
    }

    std::any get(const char* key) const {
        Key k = convertKey(key);
        return getImpl(k);
    }

    // put
    void put(const std::string* key, const std::any& value) {
        Key k = convertKey(key);
        putImpl(k, value);
    }

    void put(const char* key, const std::any& value) {
        Key k = convertKey(key);
        putImpl(k, value);
    }

    // remove
    void remove(const std::string* key) {
        Key k = convertKey(key);
        removeImpl(k);
    }

    void remove(const char* key) {
        Key k = convertKey(key);
        removeImpl(k);
    }

    // keySet – returns keys in insertion order, null represented as std::nullopt
    std::vector<Key> keySet() const {
        std::vector<Key> result;
        result.reserve(order_.size());
        for (const auto& k : order_) {
            result.push_back(k);
        }
        return result;
    }

    size_t size() const {
        return data_.size();
    }

private:
    // -------- internal conversion helpers --------
    Key convertKey(const std::string* key) const {
        if (key == nullptr) {
            return std::nullopt;
        }
        return toCamelCase(*key);
    }

    Key convertKey(const char* key) const {
        if (key == nullptr) {
            return std::nullopt;
        }
        std::string s(key);
        return toCamelCase(s);
    }

    static std::string toCamelCase(const std::string& key) {
        std::vector<std::string> parts;
        size_t start = 0;
        size_t end = 0;
        while ((end = key.find('_', start)) != std::string::npos) {
            parts.push_back(key.substr(start, end - start));
            start = end + 1;
        }
        parts.push_back(key.substr(start));

        std::string result = parts[0];
        for (size_t i = 1; i < parts.size(); ++i) {
            if (!parts[i].empty()) {
                result += static_cast<char>(std::toupper(parts[i][0]));
                for (size_t j = 1; j < parts[i].size(); ++j) {
                    result += static_cast<char>(std::tolower(parts[i][j]));
                }
            }
        }
        return result;
    }

    // -------- internal data store helpers --------
    struct KeyHash {
        size_t operator()(const Key& k) const {
            if (!k.has_value()) {
                return 0;
            }
            return std::hash<std::string>()(*k);
        }
    };

    struct KeyEqual {
        bool operator()(const Key& a, const Key& b) const {
            if (a.has_value() != b.has_value()) {
                return false;
            }
            if (!a.has_value() && !b.has_value()) {
                return true;
            }
            return *a == *b;
        }
    };

    // data_ stores: key -> (value, iterator to key in order_)
    std::unordered_map<Key, std::pair<std::any, std::list<Key>::iterator>, KeyHash, KeyEqual> data_;
    std::list<Key> order_;   // insertion order

    std::any getImpl(const Key& k) const {
        auto it = data_.find(k);
        if (it == data_.end()) {
            return std::any();   // Java null
        }
        return it->second.first;
    }

    void putImpl(const Key& k, const std::any& value) {
        auto it = data_.find(k);
        if (it == data_.end()) {
            // new key – add to order, insert into map
            order_.push_back(k);
            auto last = std::prev(order_.end());
            data_[k] = std::make_pair(value, last);
        } else {
            // existing key – just update value, order unchanged
            it->second.first = value;
        }
    }

    void removeImpl(const Key& k) {
        auto it = data_.find(k);
        if (it == data_.end()) {
            return;
        }
        // remove from order list
        order_.erase(it->second.second);
        // remove from map
        data_.erase(it);
    }
};