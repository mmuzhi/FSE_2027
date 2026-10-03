#include <map>
#include <string>
#include <cctype>
#include <stdexcept>

class CamelCaseMap {
private:
    std::map<std::string, std::string> _data;

    static std::string title_string(const std::string& s) {
        std::string result;
        bool in_word = false;
        bool first_cased = true;
        for (char c : s) {
            unsigned char uc = static_cast<unsigned char>(c);
            if (std::isalpha(uc)) {
                if (!in_word) {
                    in_word = true;
                    first_cased = true;
                }
                if (first_cased) {
                    result += static_cast<char>(std::toupper(uc));
                    first_cased = false;
                } else {
                    result += static_cast<char>(std::tolower(uc));
                }
            } else {
                result += c;
                in_word = false;
            }
        }
        return result;
    }

    static std::string _to_camel_case(const std::string& key) {
        std::string result;
        std::string::size_type start = 0;
        std::string::size_type end = key.find('_');
        
        if (end == std::string::npos) {
            return key;
        }

        result += key.substr(start, end - start);

        while (end != std::string::npos) {
            start = end + 1;
            end = key.find('_', start);
            std::string part = (end == std::string::npos) ? key.substr(start) : key.substr(start, end - start);
            result += title_string(part);
        }

        return result;
    }

    std::string _convert_key(const std::string& key) const {
        return _to_camel_case(key);
    }

public:
    CamelCaseMap() = default;

    std::string& at(const std::string& key) {
        return _data.at(_convert_key(key));
    }

    const std::string& at(const std::string& key) const {
        return _data.at(_convert_key(key));
    }

    std::string& operator[](const std::string& key) {
        return _data[_convert_key(key)];
    }

    void erase(const std::string& key) {
        std::string converted = _convert_key(key);
        if (_data.find(converted) == _data.end()) {
            throw std::out_of_range("KeyError");
        }
        _data.erase(converted);
    }

    std::map<std::string, std::string>::iterator begin() {
        return _data.begin();
    }

    std::map<std::string, std::string>::iterator end() {
        return _data.end();
    }

    std::map<std::string, std::string>::const_iterator begin() const {
        return _data.begin();
    }

    std::map<std::string, std::string>::const_iterator end() const {
        return _data.end();
    }

    size_t size() const {
        return _data.size();
    }
};