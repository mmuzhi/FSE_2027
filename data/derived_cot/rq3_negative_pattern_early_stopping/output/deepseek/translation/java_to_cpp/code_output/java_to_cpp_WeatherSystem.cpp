#include <string>
#include <unordered_map>
#include <optional>
#include <variant>
#include <vector>
#include <memory>

class WeatherSystem {
private:
    std::optional<double> temperature;
    std::string weather;
    std::string city;
    std::unordered_map<std::string, std::unordered_map<std::string, std::variant<double, std::string>>> weatherList;

public:
    WeatherSystem(const std::string& city) : city(city) {}

    void setCity(const std::string& city) {
        this->city = city;
    }

    std::string getCity() const {
        return city;
    }

    void setTemperature(double temperature) {
        this->temperature = temperature;
    }

    double celsiusToFahrenheit() const {
        return (*temperature * 9.0 / 5.0) + 32.0;
    }

    double fahrenheitToCelsius() const {
        return (*temperature - 32.0) * 5.0 / 9.0;
    }

    std::variant<bool, std::pair<double, std::string>> query(
        const std::unordered_map<std::string, std::unordered_map<std::string, std::variant<double, std::string>>>& weatherList,
        const std::string& tmpUnits)
    {
        this->weatherList = weatherList;
        auto it = weatherList.find(city);
        if (it == weatherList.end()) {
            return false;
        }

        const auto& cityWeather = it->second;
        auto tempIt = cityWeather.find("temperature");
        if (tempIt != cityWeather.end()) {
            temperature = std::get<double>(tempIt->second);
        } else {
            temperature.reset();
        }

        auto weatherIt = cityWeather.find("weather");
        if (weatherIt != cityWeather.end()) {
            weather = std::get<std::string>(weatherIt->second);
        } else {
            weather.clear();
        }

        auto unitsIt = cityWeather.find("temperature units");
        std::string currentUnits;
        if (unitsIt != cityWeather.end()) {
            currentUnits = std::get<std::string>(unitsIt->second);
        }

        if (currentUnits != tmpUnits) {
            if (tmpUnits == "celsius") {
                temperature = fahrenheitToCelsius();
            } else if (tmpUnits == "fahrenheit") {
                temperature = celsiusToFahrenheit();
            }
        }

        return std::make_pair(*temperature, weather);
    }
};