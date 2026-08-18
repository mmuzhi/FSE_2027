// This is a class as utility for managing and manipulating Cookies,
// including methods for retrieving, saving, and setting Cookies data.

#include <fstream>
#include <optional>
#include <stdexcept>
#include <string>
#include <utility>

#include <nlohmann/json.hpp>

using json = nlohmann::ordered_json;  // preserves insertion order like a Python dict

class CookiesUtil {
private:
    // Serializes JSON exactly like Python's json.dump default formatting
    // (", " and ": " separators, no trailing newline).
    static std::string py_dump(const json& data) {
        switch (data.type()) {
            case json::value_t::object: {
                std::string out = "{";
                bool first = true;
                for (auto it = data.begin(); it != data.end(); ++it) {
                    if (!first) out += ", ";
                    first = false;
                    out += json(it.key()).dump();
                    out += ": ";
                    out += py_dump(it.value());
                }
                out += "}";
                return out;
            }
            case json::value_t::array: {
                std::string out = "[";
                bool first = true;
                for (const auto& elem : data) {
                    if (!first) out += ", ";
                    first = false;
                    out += py_dump(elem);
                }
                out += "]";
                return out;
            }
            default:
                return data.dump();
        }
    }

public:
    std::string cookies_file;
    std::optional<json> cookies;  // None in Python

    // Initializes the CookiesUtil with the specified cookies file.
    explicit CookiesUtil(std::string cookies_file_)
        : cookies_file(std::move(cookies_file_)) {}

    // Gets the cookies from the specified response, and saves it to cookies_file.
    void get_cookies(const json& reponse) {
        cookies = reponse.at("cookies");  // throws (like KeyError) if missing
        _save_cookies();
    }

    // Loads the cookies from the cookies_file to the cookies data.
    json load_cookies() const {
        std::ifstream file(cookies_file);
        if (!file) {
            return json::object();  // FileNotFoundError -> {}
        }
        return json::parse(file);  // parse errors propagate like JSONDecodeError
    }

    // Saves the cookies to the cookies_file; returns true if successful, false otherwise.
    bool _save_cookies() const {
        try {
            std::ofstream file(cookies_file, std::ios::out | std::ios::trunc);
            if (!file) {
                return false;
            }
            file << py_dump(cookies.value_or(json()));
            file.close();
            return !file.fail();
        } catch (...) {
            return false;
        }
    }

    // Sets request['cookies'] = "key1=value1; key2=value2"
    void set_cookies(json& request) const {
        if (!cookies.has_value() || !cookies->is_object()) {
            // self.cookies is None (or not a dict): Python raises AttributeError
            throw std::runtime_error("'NoneType' object has no attribute 'items'");
        }
        std::string joined;
        bool first = true;
        for (auto it = cookies->begin(); it != cookies->end(); ++it) {
            if (!first) joined += "; ";
            first = false;
            std::string value_str =
                it.value().is_string() ? it.value().get<std::string>() : it.value().dump();
            joined += it.key() + "=" + value_str;
        }
        request["cookies"] = joined;
    }
};