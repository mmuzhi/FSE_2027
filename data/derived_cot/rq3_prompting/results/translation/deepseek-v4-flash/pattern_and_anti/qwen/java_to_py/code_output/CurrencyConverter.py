class CurrencyConverter:
    def __init__(self):
        self.rates = {
            "USD": 1.0,
            "EUR": 0.85,
            "GBP": 0.72,
            "JPY": 110.15,
            "CAD": 1.23,
            "AUD": 1.34,
            "CNY": 6.40,
        }

    def convert(self, amount, fromCurrency, toCurrency):
        amount = float(amount)
        if fromCurrency == toCurrency:
            return amount

        if fromCurrency not in self.rates or toCurrency not in self.rates:
            return -1.0

        fromRate = self.rates[fromCurrency]
        toRate = self.rates[toCurrency]

        return (amount / fromRate) * toRate

    def getSupportedCurrencies(self):
        return self.rates.keys()

    def addCurrencyRate(self, currency, rate):
        if currency in self.rates:
            return False
        self.rates[currency] = float(rate)
        return True

    def updateCurrencyRate(self, currency, newRate):
        if currency not in self.rates:
            return False
        self.rates[currency] = float(newRate)
        return True

    def getRates(self):
        return self.rates