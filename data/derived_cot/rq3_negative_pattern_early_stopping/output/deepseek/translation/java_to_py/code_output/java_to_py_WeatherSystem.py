class WeatherSystem:
    def __init__(self, city: str):
        self.city = city
        self.temperature = None          # double, can be None
        self.weather = None              # string, can be None
        self.weatherList = {}            # dict of dicts

    def setCity(self, city: str):
        self.city = city

    def getCity(self) -> str:
        return self.city

    def setTemperature(self, temperature: float):
        self.temperature = temperature

    def celsiusToFahrenheit(self) -> float:
        return (self.temperature * 9 / 5) + 32

    def fahrenheitToCelsius(self) -> float:
        return (self.temperature - 32) * 5 / 9

    def query(self, weatherList: dict, tmpUnits: str) -> list:
        """
        Returns a list mimicking Java's Object[].
        If city not found: [False]
        If found: [temperature, weather] after possible unit conversion.
        """
        self.weatherList = weatherList
        if self.city not in weatherList:
            return [False]

        city_weather = weatherList[self.city]
        self.temperature = city_weather["temperature"]   # assumes key exists
        self.weather = city_weather["weather"]           # assumes key exists
        current_units = city_weather["temperature units"]  # assumes key exists

        if current_units != tmpUnits:
            if tmpUnits == "celsius":
                self.temperature = self.fahrenheitToCelsius()
            elif tmpUnits == "fahrenheit":
                self.temperature = self.celsiusToFahrenheit()

        return [self.temperature, self.weather]