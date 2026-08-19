#include <any>
#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

class WeatherSystem {
private:
    std::optional<double> temperature; // Java Double: nullable
    std::string weather;
    std::string city;
    std::unordered_map<std::string, std::unordered_map<std::string, std::any>> weatherList;

public:
    explicit WeatherSystem(const std::string& city)
        : city(city) {}

    void setCity(const std::string& city) {
        this->city = city;
    }

    const std::string& getCity() const {
        return this->city;
    }

    void setTemperature(const std::optional<double>& temperature) {
        this->temperature = temperature;
    }

    double celsiusToFahrenheit() {
        return (this->temperature.value() * 9 / 5) + 32; // .value() ~ NullPointerException on null
    }

    double fahrenheitToCelsius() {
        return (this->temperature.value() - 32) * 5 / 9;
    }

    std::vector<std::any> query(const std::unordered_map<std::string, std::unordered_map<std::string, std::any>>& weatherList,
                                const std::string& tmpUnits) {
        this->weatherList = weatherList;
        auto it = weatherList.find(this->city);
        if (it == weatherList.end()) {
            return {std::any(false)};
        }

        const auto& cityWeather = it->second;
        this->temperature = std::any_cast<double>(cityWeather.at("temperature"));     // bad_any_cast ~ ClassCastException
        this->weather = std::any_cast<std::string>(cityWeather.at("weather"));
        std::string currentUnits = std::any_cast<std::string>(cityWeather.at("temperature units"));

        if (currentUnits != tmpUnits) {
            if (tmpUnits == "celsius") {
                this->temperature = fahrenheitToCelsius();
            } else if (tmpUnits == "fahrenheit") {
                this->temperature = celsiusToFahrenheit();
            }
        }

        return {std::any(this->temperature.value()), std::any(this->weather)};
    }
};