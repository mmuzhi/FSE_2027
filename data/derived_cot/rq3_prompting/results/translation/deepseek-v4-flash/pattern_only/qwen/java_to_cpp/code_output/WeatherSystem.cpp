#include <any>
#include <optional>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

using WeatherData = std::unordered_map<std::string, std::any>;
using CityWeather = std::optional<WeatherData>;
using WeatherList = std::unordered_map<std::string, CityWeather>;

class WeatherSystem {
private:
    std::optional<double> temperature;
    std::optional<std::string> weather;
    std::string city;
    WeatherList weatherList;

public:
    WeatherSystem(const std::string& city) : city(city) {}

    void setCity(const std::string& city) {
        this->city = city;
    }

    std::string getCity() const {
        return city;
    }

    void setTemperature(std::optional<double> temperature) {
        this->temperature = temperature;
    }

    double celsiusToFahrenheit() const {
        return (temperature.value() * 9 / 5) + 32;
    }

    double fahrenheitToCelsius() const {
        return (temperature.value() - 32) * 5 / 9;
    }

    std::vector<std::any> query(const WeatherList& weatherList,
                                const std::optional<std::string>& tmpUnits) {
        this->weatherList = weatherList;

        auto cityIt = weatherList.find(city);
        if (cityIt == weatherList.end()) {
            return {false};
        }

        const CityWeather& cityWeatherOpt = cityIt->second;
        if (!cityWeatherOpt.has_value()) {
            throw std::runtime_error("NullPointerException");
        }
        const WeatherData& cityWeather = *cityWeatherOpt;

        auto tempIt = cityWeather.find("temperature");
        if (tempIt == cityWeather.end() || !tempIt->second.has_value()) {
            temperature = std::nullopt;
        } else {
            temperature = std::any_cast<double>(tempIt->second);
        }

        auto weatherIt = cityWeather.find("weather");
        if (weatherIt == cityWeather.end() || !weatherIt->second.has_value()) {
            weather = std::nullopt;
        } else {
            weather = std::any_cast<std::string>(weatherIt->second);
        }

        auto unitsIt = cityWeather.find("temperature units");
        if (unitsIt == cityWeather.end() || !unitsIt->second.has_value()) {
            throw std::runtime_error("NullPointerException");
        }
        std::string currentUnits = std::any_cast<std::string>(unitsIt->second);

        if (!tmpUnits.has_value() || currentUnits != *tmpUnits) {
            if (!tmpUnits.has_value()) {
                throw std::runtime_error("NullPointerException");
            }
            if (*tmpUnits == "celsius") {
                temperature = fahrenheitToCelsius();
            } else if (*tmpUnits == "fahrenheit") {
                temperature = celsiusToFahrenheit();
            }
        }

        std::vector<std::any> result;
        if (temperature.has_value()) {
            result.push_back(temperature.value());
        } else {
            result.push_back(std::any{});
        }
        if (weather.has_value()) {
            result.push_back(weather.value());
        } else {
            result.push_back(std::any{});
        }
        return result;
    }
};