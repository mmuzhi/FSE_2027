#include <string>
#include <map>
#include <optional>
#include <utility>

class WeatherSystem {
public:
    struct WeatherInfo {
        std::string weather;
        double temperature;
        std::string temperature_units;
    };

private:
    double temperature;
    std::string weather;
    std::string city;
    std::map<std::string, WeatherInfo> weather_list;

public:
    WeatherSystem(const std::string& city)
        : temperature(0.0), weather(""), city(city), weather_list() {}

    std::optional<std::pair<double, std::string>> query(
        const std::map<std::string, WeatherInfo>& weather_list,
        const std::string& tmp_units = "celsius") {
        this->weather_list = weather_list;
        auto it = this->weather_list.find(city);
        if (it == this->weather_list.end()) {
            return std::nullopt;
        }
        const WeatherInfo& info = it->second;
        this->temperature = info.temperature;
        this->weather = info.weather;
        if (info.temperature_units != tmp_units) {
            if (tmp_units == "celsius") {
                return std::make_pair(fahrenheit_to_celsius(), this->weather);
            } else if (tmp_units == "fahrenheit") {
                return std::make_pair(celsius_to_fahrenheit(), this->weather);
            }
        }
        return std::make_pair(this->temperature, this->weather);
    }

    void set_city(const std::string& new_city) {
        city = new_city;
    }

    double celsius_to_fahrenheit() {
        return (temperature * 9.0 / 5.0) + 32.0;
    }

    double fahrenheit_to_celsius() {
        return (temperature - 32.0) * 5.0 / 9.0;
    }
};