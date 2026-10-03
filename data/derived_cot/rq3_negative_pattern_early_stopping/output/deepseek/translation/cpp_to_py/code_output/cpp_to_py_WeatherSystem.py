from copy import deepcopy

class WeatherInfo:
    """Replicates the C++ struct WeatherInfo."""
    def __init__(self, weather: str, temperature: float, temperature_units: str):
        self.weather = weather
        self.temperature = temperature
        self.temperature_units = temperature_units


class WeatherSystem:
    def __init__(self, city: str):
        self.city = city
        self.temperature = 0.0
        self.weather = ""
        self.weather_list = {}  # will be filled by query()

    def query(self, weather_list: dict, tmp_units: str = "celsius"):
        """
        Stores a copy of the given weather_list, then looks up the current city.
        Returns (temperature, weather) after possible unit conversion.
        Behaviour identical to the C++ version, including the undefined case
        when tmp_units differs from stored units but is neither "celsius" nor "fahrenheit".
        """
        self.weather_list = {
            city: WeatherInfo(info.weather, info.temperature, info.temperature_units)
            for city, info in weather_list.items()
        }

        entry = self.weather_list.get(self.city)
        if entry is None:
            return (0.0, "")

        self.temperature = entry.temperature
        self.weather = entry.weather

        if entry.temperature_units != tmp_units:
            if tmp_units == "celsius":
                return (self.fahrenheit_to_celsius(), self.weather)
            elif tmp_units == "fahrenheit":
                return (self.celsius_to_fahrenheit(), self.weather)
        else:
            return (self.temperature, self.weather)

    def set_city(self, city: str):
        self.city = city

    def set_temperature(self, temperature: float):
        self.temperature = temperature

    def celsius_to_fahrenheit(self) -> float:
        return (self.temperature * 9.0 / 5.0) + 32.0

    def fahrenheit_to_celsius(self) -> float:
        return (self.temperature - 32.0) * 5.0 / 9.0

    def get_city(self) -> str:
        return self.city