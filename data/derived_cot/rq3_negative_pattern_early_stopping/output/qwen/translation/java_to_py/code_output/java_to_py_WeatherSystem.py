class NullPointerException(Exception):
    pass

class WeatherSystem:
    def __init__(self, city):
        self.city = city
        self.weather_list = {}
        self.temperature = None
        self.weather = None

    def setCity(self, city):
        self.city = city

    def setTemperature(self, temperature):
        self.temperature = temperature

    def celsiusToFahrenheit(self):
        if self.temperature is None:
            raise Exception("Temperature is not set")
        return (self.temperature * 9 / 5) + 32

    def fahrenheitToCelsius(self):
        if self.temperature is None:
            raise Exception("Temperature is not set")
        return (self.temperature - 32) * 5 / 9

    def query(self, weather_list, tmp_units):
        self.weather_list = weather_list

        if self.city not in self.weather_list:
            return [False]

        city_weather = self.weather_list[self.city]

        def get_key(d, key):
            if key not in d:
                raise NullPointerException(f"{key} is null")
            return d[key]

        try:
            self.temperature = get_key(city_weather, "temperature")
            self.weather = get_key(city_weather, "weather")
            current_units = get_key(city_weather, "temperature units")
        except KeyError:
            pass

        if current_units != tmp_units:
            if tmp_units == "celsius":
                self.temperature = self.fahrenheitToCelsius()
            elif tmp_units == "fahrenheit":
                self.temperature = self.celsiusToFahrenheit()

        return [self.temperature, self.weather]