#include <any>
#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

namespace org::example {

class WeatherSystem {
private:
    std::optional<double> temperature; // Java's nullable Double
    std::string weather;
    std::string city;
    std::unordered_map<std::string, std::unordered_map<std::string, std::any>> weatherList;

public:
    explicit WeatherSystem(const std::string& city)
        : city(city) {
        this->weatherList = {};
    }

    void setCity(const std::string& city) {
        this->city = city;
    }

    const std::string& getCity() const {
        return this->city;
    }

    void setTemperature(std::optional<double> temperature) {
        this->temperature = temperature;
    }

    double celsiusToFahrenheit() const {
        // .value() throws (like unboxing a null Double throws NullPointerException)
        return (this->temperature.value() * 9 / 5) + 32;
    }

    double fahrenheitToCelsius() const {
        return (this->temperature.value() - 32) * 5 / 9;
    }

    std::vector<std::any> query(const std::unordered_map<std::string, std::unordered_map<std::string, std::any>>& weatherList,
                                const std::string& tmpUnits) {
        this->weatherList = weatherList;
        auto it = weatherList.find(this->city);
        if (it == weatherList.end()) {
            return {std::any(false)};
        }

        const std::unordered_map<std::string, std::any>& cityWeather = it->second;
        // any_cast throws std::bad_any_cast on a wrong type (analog of ClassCastException)
        this->temperature = std::any_cast<double>(cityWeather.at("temperature"));
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

} // namespace org::example