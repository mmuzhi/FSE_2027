#include <string>
#include <unordered_map>
#include <optional>
#include <variant>
#include <utility>

struct CityWeather {
    std::string weather;
    double temperature = 0.0;
    std::string temperature_units;
};

using QueryResult = std::variant<std::monostate, bool, std::pair<double, std::string>>;

struct WeatherSystem {
    WeatherSystem(const std::string& city) : city(city) {}

    QueryResult query(const std::unordered_map<std::string, CityWeather>& weather_list,
                      const std::string& tmp_units = "celsius") {
        this->weather_list = weather_list;
        auto it = this->weather_list.find(city);
        if (it == this->weather_list.end()) {
            return false;
        }
        const CityWeather& city_weather = it->second;
        temperature = city_weather.temperature;
        weather = city_weather.weather;

        if (city_weather.temperature_units != tmp_units) {
            if (tmp_units == "celsius") {
                return std::make_pair(fahrenheit_to_celsius(), weather.value());
            } else if (tmp_units == "fahrenheit") {
                return std::make_pair(celsius_to_fahrenheit(), weather.value());
            } else {
                return std::monostate{};
            }
        } else {
            return std::make_pair(temperature.value(), weather.value());
        }
    }

    void set_city(const std::string& city) {
        this->city = city;
    }

    double celsius_to_fahrenheit() const {
        return (temperature.value() * 9.0 / 5.0) + 32.0;
    }

    double fahrenheit_to_celsius() const {
        return (temperature.value() - 32.0) * 5.0 / 9.0;
    }

    std::optional<double> temperature;
    std::optional<std::string> weather;
    std::string city;
    std::unordered_map<std::string, CityWeather> weather_list;
};