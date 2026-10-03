#include <iostream>
#include <map>
#include <optional>
#include <string>

class WeatherSystem {
private:
    std::string city;
    double temperature;
    std::string weather;
    std::map<std::string, std::map<std::string, std::string>> weather_list;

public:
    WeatherSystem(std::string city) : city(city), temperature(nullptr), weather(nullptr) {}

    std::optional<std::pair<double, std::string>> query(std::map<std::string, std::map<std::string, std::string>> weather_list, std::string tmp_units = "celsius") {
        this->weather_list = weather_list;

        if (this->weather_list.find(city) == this->weather_list.end()) {
            return std::nullopt;
        }

        std::map<std::string, std::string> inner_map = this->weather_list[city];
        temperature = std::stod(inner_map["temperature"]);
        weather = inner_map["weather"];
        std::string units = inner_map["temperature units"];

        if (units != tmp_units) {
            if (tmp_units == "celsius") {
                // Convert from the original units to Celsius
                // But note: the original units could be either Celsius or Fahrenheit.
                // We don't know which one, but the condition is based on the weather_list's units.
                // However, the conversion methods are defined to convert from their name's unit to the other.
                // But we are storing the temperature in the member as the value from the weather_list, and then converting it to the desired units.
                // The desired units is 'celsius', so we need to convert from the original units to Celsius.

                // How do we know the original units? We have the 'units' string.

                // But the conversion methods are only for Celsius to Fahrenheit and Fahrenheit to Celsius.

                // We can do:

                //   If the original units are 'celsius', then we don't need to convert? But the condition is that they are not equal, so if the desired is 'celsius' and the original is 'fahrenheit', then we convert from Fahrenheit to Celsius.

                //   So we can use the `fahrenheit_to_celsius` method if the original units are 'fahrenheit', and if the original units are 'celsius', then we don't convert? But wait, the condition is that they are not equal, so if the original is 'celsius' and desired is 'celsius', we wouldn't be here.

                //   So in this branch, the original units are not 'celsius' (because the condition is not equal). The only other option is 'fahrenheit'. So we convert from Fahrenheit to Celsius.

                //   But wait, what if the weather_list uses a different unit? The problem says the parameter tmp_units is either 'celsius' or 'fahrenheit'. And the weather_list's units are either 'celsius' or 'fahrenheit'. So we can assume that.

                //   Therefore, if the desired units are 'celsius' and the original units are not 'celsius', then they must be 'fahrenheit'. So we convert from Fahrenheit to Celsius.

                return std::make_pair(fahrenheit_to_celsius(), weather);
            } else if (tmp_units == "fahrenheit") {
                // Convert from the original units to Fahrenheit
                // The original units are not 'fahrenheit' (because the condition is not equal), so they must be 'celsius'
                return std::make_pair(celsius_to_fahrenheit(), weather);
            }
        } else {
            // The units match, so return the temperature and weather without conversion
            return std::make_pair(temperature, weather);
        }
    }

    void set_city(std::string city) {
        this->city = city;
    }

    double celsius_to_fahrenheit() {
        return (temperature * 9.0 / 5.0) + 32.0;
    }

    double fahrenheit_to_celsius() {
        return (temperature - 32.0) * 5.0 / 9.0;
    }
};