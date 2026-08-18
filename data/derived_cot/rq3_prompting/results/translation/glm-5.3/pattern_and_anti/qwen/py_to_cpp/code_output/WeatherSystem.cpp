#include <string>
#include <utility>
#include <variant>
#include <optional>
#include <unordered_map>
#include <stdexcept>

class WeatherSystem {
public:
    struct CityInfo {
        std::string weather;
        double temperature;
        std::string temperature_units;  // 'temperature units'
    };

    using WeatherList = std::unordered_map<std::string, CityInfo>;
    // Mirrors Python returns: None (monostate), False (bool), or (temperature, weather) tuple.
    using QueryResult = std::variant<std::monostate, bool, std::pair<double, std::string>>;

    explicit WeatherSystem(const std::string& city)
        : temperature(std::nullopt), weather(std::nullopt), city(city) {}

    QueryResult query(const WeatherList& weather_list, const std::string& tmp_units = "celsius") {
        this->weather_list = weather_list;
        auto it = this->weather_list.find(city);
        if (it == this->weather_list.end()) {
            return false;
        }
        temperature = it->second.temperature;
        weather = it->second.weather;
        if (it->second.temperature_units != tmp_units) {
            if (tmp_units == "celsius") {
                return std::make_pair(fahrenheit_to_celsius(), *weather);
            } else if (tmp_units == "fahrenheit") {
                return std::make_pair(celsius_to_fahrenheit(), *weather);
            }
            return std::monostate{};  // implicit None fall-through
        }
        return std::make_pair(*temperature, *weather);
    }

    void set_city(const std::string& city) {
        this->city = city;
    }

    double celsius_to_fahrenheit() const {
        require_temperature();
        return (*temperature * 9.0 / 5.0) + 32.0;
    }

    double fahrenheit_to_celsius() const {
        require_temperature();
        return (*temperature - 32.0) * 5.0 / 9.0;
    }

    // Public state, mirroring the Python instance attributes.
    std::optional<double> temperature;        // None -> nullopt
    std::optional<std::string> weather;       // None -> nullopt
    std::string city;
    WeatherList weather_list;

private:
    void require_temperature() const {
        if (!temperature.has_value()) {
            // Python raises TypeError on None arithmetic.
            throw std::runtime_error("TypeError: unsupported operand type(s): temperature is None");
        }
    }
};