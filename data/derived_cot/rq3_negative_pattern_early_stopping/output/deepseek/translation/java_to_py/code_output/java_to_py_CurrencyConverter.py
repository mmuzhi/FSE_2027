class CurrencyConverter:
    def __init__(self):
        self.rates = {
            "USD": 1.0,
            "EUR": 0.85,
            "GBP": 0.72,
            "JPY": 110.15,
            "CAD": 1.23,
            "AUD": 1.34,
            "CNY": 6.40
        }

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        if from_currency == to_currency:
            return amount

        if from_currency not in self.rates or to_currency not in self.rates:
            return -1.0

        from_rate = self.rates[from_currency]
        to_rate = self.rates[to_currency]

        converted_amount = (amount / from_rate) * to_rate
        return converted_amount

    def get_supported_currencies(self):
        return set(self.rates.keys())

    def add_currency_rate(self, currency: str, rate: float) -> bool:
        if currency in self.rates:
            return False
        self.rates[currency] = rate
        return True

    def update_currency_rate(self, currency: str, new_rate: float) -> bool:
        if currency not in self.rates:
            return False
        self.rates[currency] = new_rate
        return True

    def get_rates(self):
        return self.rates