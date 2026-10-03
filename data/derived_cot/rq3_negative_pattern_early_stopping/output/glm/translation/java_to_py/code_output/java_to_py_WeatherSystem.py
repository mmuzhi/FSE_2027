class WeatherSystem:
    def __init__(self, city):
        self.temperature = None
        self.weather = None
        self.city = city
        self.weather_list = {}

    def set_city(self, city):
        self.city = city

    def get_city(self):
        return self.city

    def set_temperature(self, temperature):
        self.temperature = temperature

    def celsius_to_fahrenheit(self):
        return (self.temperature * 9 / 5) + 32

    def fahrenheit_to_celsius(self):
        return (self.temperature - 32) * 5 / 9

    def query(self, weather_list, tmp_units):
        self.weather_list = weather_list
        if self.city not in weather_list:
            return [False]

        city_weather = weather_list[self.city]
        self.temperature = city_weather["temperature"]
        self.weather = city_weather["weather"]
        current_units = city_weather["temperature units"]

        if current_units != tmp_units:
            if tmp_units == "celsius":
                self.temperature = self.fahrenheit_to_celsius()
            elif tmp_units == "fahrenheit":
                self.temperature = self.celsius_to_fahrenheit()

        return [self.temperature, self.weather]