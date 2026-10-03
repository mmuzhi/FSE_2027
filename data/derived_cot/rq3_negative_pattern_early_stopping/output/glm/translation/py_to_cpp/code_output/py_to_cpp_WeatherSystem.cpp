#include <string>
#include <unordered_map>
#include <variant>
#include <optional>
#include <utility>

class WeatherSystem {
public:
    using WeatherInfo = std::unordered_map<std::string, std::variant<std::string, double>>;
    using WeatherList = std::unordered_map<std::string, WeatherInfo>;

    std::optional<double> temperature;
    std::optional<std::string> weather;
    std::string city;
    WeatherList weather_list;

    WeatherSystem(std::string city) : city(std::move(city)) {}

    std::variant<bool, std::pair<double, std::string>> query(const WeatherList& wl, const std::string& tmp_units = "celsius") {
        weather_list = wl;
        if (weather_list.find(city) == weather_list.end()) {
            return false;
        } else {
            temperature = std::get<double>(weather_list.at(city).at("temperature"));
            weather = std::get<std::string>(weather_list.at(city).at("weather"));
        }
        if (std::get<std::string>(weather_list.at(city).at("temperature units")) != tmp_units) {
            if (tmp_units == "celsius") {
                return {fahrenheit_to_celsius(), weather.value()};
            } else if (tmp_units == "fahrenheit") {
                return {celsius_to_fahrenheit(), weather.value()};
            }
            return false;
        } else {
            return {temperature.value(), weather.value()};
        }
    }

    void set_city(const std::string& new_city) {
        city = new_city;
    }

    double celsius_to_fahrenheit() {
        return (temperature.value() * 9.0 / 5.0) + 32.0;
    }

    double fahrenheit_to_celsius() {
        return (temperature.value() - 32.0) * 5.0 / 9.0;
    }
};