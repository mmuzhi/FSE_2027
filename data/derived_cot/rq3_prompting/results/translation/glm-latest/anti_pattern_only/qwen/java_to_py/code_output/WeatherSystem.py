class WeatherSystem:
    def __init__(self, city):
        self.temperature = None
        self.weather = None
        self.city = city
        self.weatherList = {}

    def setCity(self, city):
        self.city = city

    def getCity(self):
        return self.city

    def setTemperature(self, temperature):
        self.temperature = temperature

    def celsiusToFahrenheit(self):
        return (self.temperature * 9 / 5) + 32

    def fahrenheitToCelsius(self):
        return (self.temperature - 32) * 5 / 9

    def query(self, weatherList, tmpUnits):
        self.weatherList = weatherList
        if self.city not in weatherList:
            return [False]

        cityWeather = weatherList[self.city]
        self.temperature = cityWeather.get("temperature")
        self.weather = cityWeather.get("weather")
        currentUnits = cityWeather.get("temperature units")

        if currentUnits != tmpUnits:
            if tmpUnits == "celsius":
                self.temperature = self.fahrenheitToCelsius()
            elif tmpUnits == "fahrenheit":
                self.temperature = self.celsiusToFahrenheit()

        return [self.temperature, self.weather]