#include <map>
#include <optional>
#include <stdexcept>
#include <string>
#include <utility>
#include <variant>

class WeatherSystem {
public:
    // Python dict values are str or number -> variant
    using Value = std::variant<std::string, double>;
    // Python dict-of-dicts: {city: {field: value}}
    using WeatherList = std::map<std::string, std::map<std::string, Value>>;
    // query() returns: tuple(temperature, weather) | False | None
    using QueryResult = std::variant<std::pair<double, std::string>, bool, std::monostate>;

    std::optional<double> temperature;   // None
    std::optional<std::string> weather;  // None
    std::string city;
    WeatherList weather_list;

    explicit WeatherSystem(std::string city)
        : temperature(std::nullopt), weather(std::nullopt),
          city(std::move(city)), weather_list() {}

    QueryResult query(const WeatherList& new_weather_list,
                      const std::string& tmp_units = "celsius") {
        weather_list = new_weather_list;
        auto city_it = weather_list.find(city);
        if (city_it == weather_list.end()) {
            return false;  // Python: return False
        }
        const std::map<std::string, Value>& info = city_it->second;

        temperature = as_number(info, "temperature");   // KeyError-equivalent if missing
        weather = as_string(info, "weather");

        std::string units = as_string(info, "temperature units");
        if (units != tmp_units) {
            if (tmp_units == "celsius") {
                return std::make_pair(fahrenheit_to_celsius(), *weather);
            } else if (tmp_units == "fahrenheit") {
                return std::make_pair(celsius_to_fahrenheit(), *weather);
            }
            return std::monostate{};  // Python: implicit None (unit mismatch, no branch taken)
        }
        return std::make_pair(*temperature, *weather);
    }

    void set_city(std::string new_city) { city = std::move(new_city); }

    double celsius_to_fahrenheit() const {
        require_temperature();
        return (*temperature * 9 / 5) + 32;  // same eval order as (t * 9/5) + 32
    }

    double fahrenheit_to_celsius() const {
        require_temperature();
        return (*temperature - 32) * 5 / 9;  // same eval order as (t - 32) * 5/9
    }

private:
    static const Value& field(const std::map<std::string, Value>& info, const std::string& key) {
        auto it = info.find(key);
        if (it == info.end()) throw std::out_of_range("KeyError: '" + key + "'");
        return it->second;
    }
    static double as_number(const std::map<std::string, Value>& info, const std::string& key) {
        const Value& v = field(info, key);
        if (auto* d = std::get_if<double>(&v)) return *d;
        throw std::runtime_error("TypeError: '" + key + "' is not a number");
    }
    static std::string as_string(const std::map<std::string, Value>& info, const std::string& key) {
        const Value& v = field(info, key);
        if (auto* s = std::get_if<std::string>(&v)) return *s;
        throw std::runtime_error("TypeError: '" + key + "' is not a string");
    }
    void require_temperature() const {
        if (!temperature.has_value())
            throw std::runtime_error("TypeError: unsupported operand type(s): temperature is None");
    }
};