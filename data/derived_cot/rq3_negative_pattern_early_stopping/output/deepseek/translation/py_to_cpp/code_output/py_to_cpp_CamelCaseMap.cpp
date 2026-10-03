#include <map>
#include <string>
#include <vector>
#include <stdexcept>
#include <cctype>
#include <algorithm>

template<typename T>
class CamelCaseMap {
public:
    CamelCaseMap() = default;

    T& get(const std::string& key) {
        auto it = data_.find(convert_key(key));
        if (it == data_.end()) {
            throw std::out_of_range("key not found");
        }
        return it->second;
    }

    const T& get(const std::string& key) const {
        auto it = data_.find(convert_key(key));
        if (it == data_.end()) {
            throw std::out_of_range("key not found");
        }
        return it->second;
    }

    void set(const std::string& key, const T& value) {
        data_[convert_key(key)] = value;
    }

    void del(const std::string& key) {
        auto it = data_.find(convert_key(key));
        if (it == data_.end()) {
            throw std::out_of_range("key not found");
        }
        data_.erase(it);
    }

    class Iterator {
    public:
        using map_iterator = typename std::map<std::string, T>::const_iterator;
        Iterator(map_iterator it) : it_(it) {}
        const std::string& operator*() const { return it_->first; }
        Iterator& operator++() { ++it_; return *this; }
        bool operator!=(const Iterator& other) const { return it_ != other.it_; }
    private:
        map_iterator it_;
    };

    Iterator begin() const { return Iterator(data_.begin()); }
    Iterator end() const { return Iterator(data_.end()); }

    size_t size() const { return data_.size(); }

    // _convert_key port
    std::string convert_key(const std::string& key) const {
        return to_camel_case(key);
    }

    static std::string to_camel_case(const std::string& key) {
        std::vector<std::string> parts;
        size_t start = 0, end;
        while ((end = key.find('_', start)) != std::string::npos) {
            parts.push_back(key.substr(start, end - start));
            start = end + 1;
        }
        parts.push_back(key.substr(start));
        if (parts.empty()) return "";
        std::string result = parts[0];
        for (size_t i = 1; i < parts.size(); ++i) {
            const std::string& p = parts[i];
            if (!p.empty()) {
                result += std::toupper(p[0]);
                if (p.size() > 1) {
                    result += p.substr(1);
                }
            }
        }
        return result;
    }

private:
    std::map<std::string, T> data_;
};