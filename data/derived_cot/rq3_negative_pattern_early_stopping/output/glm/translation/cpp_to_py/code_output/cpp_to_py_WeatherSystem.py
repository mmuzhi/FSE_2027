from dataclasses import dataclass
from typing import Dict, Tuple, Optional

@dataclass
class WeatherInfo:
    weather: str
    temperature: float
    temperature_units: str

class WeatherSystem:
    def __init__(self, city: str):
        self.city: str = city
        self.temperature: float = 0.0
        self.weather: str = ""
        self.weather_list: Dict[str, WeatherInfo] = {}

    def query(self, weather_list: Dict[str, WeatherInfo], tmp_units: str = "celsius") -> Optional[Tuple[float, str]]:
        self.weather_list = weather_list
        
        if self.city not in self.weather_list:
            return (0.0, "")
        else:
            info = self.weather_list[self.city]
            self.temperature = info.temperature
            self.weather = info.weather

        if info.temperature_units != tmp_units:
            if tmp_units == "celsius":
                return (self.fahrenheit_to_celsius(), self.weather)
            elif tmp_units == "fahrenheit":
                return (self.celsius_to_fahrenheit(), self.weather)
        else:
            return (self.temperature, self.weather)
        

    def set_city(self, city: str) -> None:
        self.city = city

    def set_temperature(self, temperature: float) -> None:
        self.temperature = temperature

    def celsius_to_fahrenheit(self) -> float:
        return (self.temperature * 9 / 5) + 32

    def fahrenheit_to_celsius(self) -> float:
        return (self.temperature - 32) * 5 / 9

    def get_city(self) -> str:
        return self.city