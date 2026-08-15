from collections.abc import Set as AbcSet


class UnsupportedOperationException(Exception):
    pass


class _KeySet(AbcSet):
    def __init__(self, d):
        self._d = d

    def __contains__(self, item):
        return item in self._d

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)

    def __repr__(self):
        return repr(set(self._d))

    def __hash__(self):
        return hash(frozenset(self._d))

    def add(self, item):
        raise UnsupportedOperationException()

    def remove(self, key):
        if key in self._d:
            del self._d[key]
            return True
        return False

    def discard(self, key):
        if key in self._d:
            del self._d[key]

    def clear(self):
        self._d.clear()


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
        self._key_set = None

    def convert(self, amount, fromCurrency, toCurrency):
        if fromCurrency == toCurrency:
            return amount

        if fromCurrency not in self.rates or toCurrency not in self.rates:
            return -1

        fromRate = self.rates[fromCurrency]
        toRate = self.rates[toCurrency]

        return (amount / fromRate) * toRate

    def getSupportedCurrencies(self):
        if self._key_set is None:
            self._key_set = _KeySet(self.rates)
        return self._key_set

    def addCurrencyRate(self, currency, rate):
        if currency in self.rates:
            return False
        self.rates[currency] = rate
        return True

    def updateCurrencyRate(self, currency, newRate):
        if currency not in self.rates:
            return False
        self.rates[currency] = newRate
        return True

    def getRates(self):
        return self.rates