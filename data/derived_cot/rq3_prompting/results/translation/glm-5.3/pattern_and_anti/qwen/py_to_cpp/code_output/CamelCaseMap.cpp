#include <cctype>
#include <cstddef>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

// Custom class that allows keys to be in camel case style by converting them
// from underscore style; provides dictionary-like functionality.
class CamelCaseMap {
public:
    CamelCaseMap() = default;

    // __getitem__: KeyError on missing key -> std::out_of_range
    const std::string& at(const std::string& key) const {
        const std::string converted = convert_key(key);
        for (const auto& kv : data_) {
            if (kv.first == converted) return kv.second;
        }
        throw std::out_of_range(converted);
    }

    std::string& at(const std::string& key) {
        return const_cast<std::string&>(
            static_cast<const CamelCaseMap*>(this)->at(key));
    }

    // __setitem__: insert or overwrite; preserves original insertion position
    void set(const std::string& key, const std::string& value) {
        const std::string converted = convert_key(key);
        for (auto& kv : data_) {
            if (kv.first == converted) {
                kv.second = value;
                return;
            }
        }
        data_.emplace_back(converted, value);
    }

    // __delitem__: KeyError on missing key -> std::out_of_range
    void del(const std::string& key) {
        const std::string converted = convert_key(key);
        for (auto it = data_.begin(); it != data_.end(); ++it) {
            if (it->first == converted) {
                data_.erase(it);
                return;
            }
        }
        throw std::out_of_range(converted);
    }

    // __len__
    std::size_t size() const { return data_.size(); }

    // __iter__: iteration over keys, in insertion order (like Python dict)
    class const_key_iterator {
    public:
        using iterator_category = std::forward_iterator_tag;
        using value_type = std::string;
        using reference = const std::string&;
        using pointer = const std::string*;
        using difference_type = std::ptrdiff_t;

        const_key_iterator() = default;
        explicit const_key_iterator(
            std::vector<std::pair<std::string, std::string>>::const_iterator it)
            : it_(it) {}

        reference operator*() const { return it_->first; }
        pointer operator->() const { return &it_->first; }
        const_key_iterator& operator++() { ++it_; return *this; }
        const_key_iterator operator++(int) {
            const_key_iterator tmp = *this; ++it_; return tmp;
        }
        friend bool operator==(const const_key_iterator& a, const const_key_iterator& b) {
            return a.it_ == b.it_;
        }
        friend bool operator!=(const const_key_iterator& a, const const_key_iterator& b) {
            return !(a == b);
        }

    private:
        std::vector<std::pair<std::string, std::string>>::const_iterator it_{};
    };

    const_key_iterator begin() const { return const_key_iterator(data_.begin()); }
    const_key_iterator end() const { return const_key_iterator(data_.end()); }

private:
    std::vector<std::pair<std::string, std::string>> data_;

    // _convert_key: keys are always strings here, so always camelized
    static std::string convert_key(const std::string& key) {
        return to_camel_case(key);
    }

    // _to_camel_case: split on '_', first part unchanged, rest title-cased
    static std::string to_camel_case(const std::string& key) {
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
        parts.push_back(current);  // str.split always yields a final piece

        std::string result = parts[0];
        for (std::size_t i = 1; i < parts.size(); ++i) {
            result += title(parts[i]);
        }
        return result;
    }

    // Equivalent of Python's str.title(): uppercase letter after a
    // non-letter, lowercase letter after a letter.
    static std::string title(const std::string& s) {
        std::string result;
        result.reserve(s.size());
        bool prev_alpha = false;
        for (unsigned char c : s) {
            if (std::isalpha(c)) {
                if (prev_alpha) {
                    result += static_cast<char>(std::tolower(c));
                } else {
                    result += static_cast<char>(std::toupper(c));
                }
                prev_alpha = true;
            } else {
                result += static_cast<char>(c);
                prev_alpha = false;
            }
        }
        return result;
    }
};