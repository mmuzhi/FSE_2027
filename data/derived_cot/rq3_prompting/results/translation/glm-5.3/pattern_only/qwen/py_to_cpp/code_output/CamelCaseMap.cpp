#include <cctype>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

/**
 * Custom class allowing keys in camel case style (converted from underscore
 * style), providing dictionary-like functionality. Preserves insertion order,
 * mirroring Python dict iteration semantics.
 */
class CamelCaseMap {
private:
    std::vector<std::pair<std::string, std::string>> _data;

    std::string _convert_key(const std::string& key) const {
        return _to_camel_case(key);
    }

    std::size_t _find_index(const std::string& camelKey) const {
        for (std::size_t i = 0; i < _data.size(); ++i) {
            if (_data[i].first == camelKey) {
                return i;
            }
        }
        return static_cast<std::size_t>(-1);
    }

public:
    CamelCaseMap() = default;

    // __getitem__: throws std::out_of_range on missing key (KeyError analogue)
    const std::string& get(const std::string& key) const {
        std::size_t idx = _find_index(_convert_key(key));
        if (idx == static_cast<std::size_t>(-1)) {
            throw std::out_of_range(key);
        }
        return _data[idx].second;
    }

    // __setitem__: insert or overwrite
    void set(const std::string& key, const std::string& value) {
        std::string camelKey = _convert_key(key);
        std::size_t idx = _find_index(camelKey);
        if (idx != static_cast<std::size_t>(-1)) {
            _data[idx].second = value;
        } else {
            _data.emplace_back(std::move(camelKey), value);
        }
    }

    // __delitem__: throws std::out_of_range on missing key (KeyError analogue)
    void del(const std::string& key) {
        std::size_t idx = _find_index(_convert_key(key));
        if (idx == static_cast<std::size_t>(-1)) {
            throw std::out_of_range(key);
        }
        _data.erase(_data.begin() + static_cast<std::ptrdiff_t>(idx));
    }

    // __iter__: iterate over stored (camel case) keys in insertion order
    std::vector<std::string> keys() const {
        std::vector<std::string> out;
        out.reserve(_data.size());
        for (const auto& kv : _data) {
            out.push_back(kv.first);
        }
        return out;
    }

    std::vector<std::string>::const_iterator key_begin() const {
        return keys().begin();  // note: use keys() directly for a stable range
    }

    // __len__
    std::size_t size() const {
        return _data.size();
    }

    // membership test ("in" in Python)
    bool contains(const std::string& key) const {
        return _find_index(_convert_key(key)) != static_cast<std::size_t>(-1);
    }

    // operator[] accessors mirroring Python subscript semantics
    const std::string& operator[](const std::string& key) const {
        return get(key);
    }

    struct Proxy {
        CamelCaseMap& map;
        std::string key;
        operator const std::string&() const { return map.get(key); }
        Proxy& operator=(const std::string& value) {
            map.set(key, value);
            return *this;
        }
    };

    Proxy operator[](const std::string& key) {
        return Proxy{*this, key};
    }

    // _to_camel_case: split on '_', keep first part verbatim,
    // title-case each subsequent part (first char upper, rest lower),
    // matching Python str.title() for these inputs. Empty parts contribute
    // nothing (e.g. "a__b" -> "aB").
    static std::string _to_camel_case(const std::string& key) {
        std::vector<std::string> parts;
        std::size_t start = 0;
        for (std::size_t i = 0; i <= key.size(); ++i) {
            if (i == key.size() || key[i] == '_') {
                parts.push_back(key.substr(start, i - start));
                start = i + 1;
            }
        }

        std::string result = parts[0];
        for (std::size_t i = 1; i < parts.size(); ++i) {
            std::string t = parts[i];
            if (!t.empty()) {
                t[0] = static_cast<char>(std::toupper(static_cast<unsigned char>(t[0])));
                for (std::size_t j = 1; j < t.size(); ++j) {
                    t[j] = static_cast<char>(std::tolower(static_cast<unsigned char>(t[j])));
                }
                result += t;
            }
        }
        return result;
    }
};