from typing import Any, Dict, List, Optional


class WeatherSystem:
    def __init__(self, city: str) -> None:
        self.temperature: Optional[float] = None
        self.weather: Optional[str] = None
        self.city: str = city
        self.weather_list: Dict[str, Dict[str, Any]] = {}

    def set_city(self, city: str) -> None:
        self.city = city

    def get_city(self) -> str:
        return self.city

    def set_temperature(self, temperature: Optional[float]) -> None:
        self.temperature = temperature

    def celsius_to_fahrenheit(self) -> float:
        return (self.temperature * 9 / 5) + 32

    def fahrenheit_to_celsius(self) -> float:
        return (self.temperature - 32) * 5 / 9

    def query(self, weather_list: Dict[str, Dict[str, Any]], tmp_units: str) -> List[Any]:
        self.weather_list = weather_list
        if self.city not in weather_list:
            return [False]

        city_weather = weather_list[self.city]
        self.temperature = city_weather.get("temperature")
        self.weather = city_weather.get("weather")
        current_units = city_weather.get("temperature units")

        if current_units != tmp_units:
            if tmp_units == "celsius":
                self.temperature = self.fahrenheit_to_celsius()
            elif tmp_units == "fahrenheit":
                self.temperature = self.celsius_to_fahrenheit()

        return [self.temperature, self.weather]