#include <vector>
#include <unordered_map>
#include <string>
#include <stdexcept>
#include <any>

class WeatherSystem {
private:
    std::string city;
    std::unordered_map<std::string, std::unordered_map<std::string, std::any>> weatherList;
    double temperature;
    std::string weather;

public:
    WeatherSystem(const std::string& city) : city(city) {}

    void setCity(const std::string& city) {
        this->city = city;
    }

    std::string getCity() const {
        return this->city;
    }

    void setTemperature(double temperature) {
        this->temperature = temperature;
    }

    double celsiusToFahrenheit() {
        return (this->temperature * 9 / 5) + 32;
    }

    double fahrenheitToCelsius() {
        return (this->temperature - 32) * 5 / 9;
    }

    std::vector<std::any> query(std::unordered_map<std::string, std::unordered_map<std::string, std::any>> weatherList, const std::string& tmpUnits) {
        this->weatherList = weatherList;
        if (this->weatherList.find(this->city) == this->weatherList.end()) {
            return {false};
        }

        auto& cityWeather = this->weatherList[this->city];
        if (cityWeather.find("temperature") == cityWeather.end() ||
            cityWeather.find("weather") == cityWeather.end() ||
            cityWeather.find("temperature units") == cityWeather.end()) {
            throw std::runtime_error("Missing required data");
        }

        this->temperature = std::any_cast<double>(cityWeather["temperature"]);
        this->weather = std::any_cast<std::string>(cityWeather["weather"]);
        std::string currentUnits = std::any_cast<std::string>(cityWeather["temperature units"]);

        if (currentUnits != tmpUnits) {
            if (tmpUnits == "celsius") {
                this->temperature = fahrenheitToCelsius();
            } else if (tmpUnits == "fahrenheit") {
                this->temperature = celsiusToFahrenheit();
            }
        }

        return {this->temperature, this->weather};
    }
};