#include <any>
#include <map>
#include <vector>
#include <string>
#include <stdexcept>
#include <algorithm>
#include <cctype>
#include <cstddef>
#include <type_traits>
#include <utility>

class CamelCaseMap {
public:
    // Proxy to support both reading and writing via operator[]
    class Proxy {
    public:
        Proxy(CamelCaseMap& map, std::string key)
            : map_(map), key_(std::move(key)) {}

        operator std::any() const {
            return map_.get(key_);
        }

        template <typename T>
        Proxy& operator=(T&& value) {
            map_.set(key_, std::forward<T>(value));
            return *this;
        }

        Proxy& operator=(const char* value) {
            map_.set(key_, std::string(value));
            return *this;
        }

        Proxy& operator=(const std::string& value) {
            map_.set(key_, value);
            return *this;
        }

    private:
        CamelCaseMap& map_;
        std::string key_;
    };

    CamelCaseMap() = default;

    // __getitem__ / __setitem__
    Proxy operator[](const std::string& key) {
        return Proxy(*this, key);
    }

    std::any operator[](const std::string& key) const {
        return get(key);
    }

    // __setitem__
    template <typename T>
    void set(const std::string& key, T&& value) {
        std::string ck = convert_key(key);
        if (data_.find(ck) == data_.end()) {
            keys_.push_back(ck);
        }
        data_[ck] = make_any(std::forward<T>(value));
    }

    // __getitem__
    std::any get(const std::string& key) const {
        auto it = data_.find(convert_key(key));
        if (it == data_.end()) {
            throw std::out_of_range("key not found");
        }
        return it->second;
    }

    // __delitem__
    void erase(const std::string& key) {
        std::string ck = convert_key(key);
        auto it = data_.find(ck);
        if (it == data_.end()) {
            throw std::out_of_range("key not found");
        }
        data_.erase(it);
        auto vit = std::find(keys_.begin(), keys_.end(), ck);
        if (vit != keys_.end()) {
            keys_.erase(vit);
        }
    }

    // __len__
    size_t size() const {
        return keys_.size();
    }

    // Helper for `in` semantics: exact key match, no camel-case conversion
    bool contains(const std::string& key) const {
        return data_.find(key) != data_.end();
    }

    template <typename T>
    bool contains(const T&) const {
        return false; // non-string keys never match string keys
    }

    // __iter__ (insertion order preserved)
    class KeyIterator {
    public:
        using iterator_category = std::forward_iterator_tag;
        using value_type = std::string;
        using difference_type = std::ptrdiff_t;
        using pointer = const std::string*;
        using reference = const std::string&;

        KeyIterator(std::vector<std::string>::const_iterator it) : it_(it) {}

        reference operator*() const { return *it_; }
        pointer operator->() const { return &(*it_); }

        KeyIterator& operator++() { ++it_; return *this; }
        KeyIterator operator++(int) { KeyIterator tmp = *this; ++it_; return tmp; }

        bool operator==(const KeyIterator& other) const { return it_ == other.it_; }
        bool operator!=(const KeyIterator& other) const { return it_ != other.it_; }

    private:
        std::vector<std::string>::const_iterator it_;
    };

    KeyIterator begin() const { return KeyIterator(keys_.begin()); }
    KeyIterator end() const { return KeyIterator(keys_.end()); }

    // _convert_key
    std::string convert_key(const std::string& key) const {
        return to_camel_case(key);
    }

    std::string convert_key(const char* key) const {
        return to_camel_case(key);
    }

    template <typename T>
    T convert_key(const T& key) const {
        return key;
    }

    // _to_camel_case
    static std::string to_camel_case(const std::string& key) {
        std::string result;
        size_t start = 0;
        bool first = true;

        while (true) {
            size_t pos = key.find('_', start);
            std::string part = key.substr(
                start,
                pos == std::string::npos ? std::string::npos : pos - start
            );

            if (first) {
                result += part;
                first = false;
            } else {
                result += title(part);
            }

            if (pos == std::string::npos) {
                break;
            }
            start = pos + 1;
        }

        return result;
    }

private:
    template <typename T>
    static std::any make_any(T&& value) {
        using Decay = std::decay_t<T>;

        if constexpr (std::is_same_v<Decay, const char*> ||
                      std::is_same_v<Decay, char*>) {
            return std::any(std::string(value));
        } else if constexpr (std::is_same_v<Decay, Proxy>) {
            return std::any(static_cast<std::any>(value));
        } else {
            return std::any(std::forward<T>(value));
        }
    }

    static std::string title(const std::string& s) {
        std::string res = s;
        bool in_word = false;

        for (size_t i = 0; i < res.size(); ++i) {
            unsigned char c = static_cast<unsigned char>(res[i]);
            if (std::isalpha(c)) {
                if (!in_word) {
                    res[i] = static_cast<char>(std::toupper(c));
                    in_word = true;
                } else {
                    res[i] = static_cast<char>(std::tolower(c));
                }
            } else {
                in_word = false;
            }
        }

        return res;
    }

    std::map<std::string, std::any> data_;
    std::vector<std::string> keys_;
};