import math
import struct
from decimal import Decimal


def _double_equals(a, b):
    if math.isnan(a) and math.isnan(b):
        return True
    if a == b:
        if a == 0.0 and b == 0.0:
            return math.copysign(1.0, a) == math.copysign(1.0, b)
        return True
    return False


def _java_string_hash(s):
    h = 0
    utf16 = s.encode('utf-16-le')
    for i in range(0, len(utf16), 2):
        unit = utf16[i] | (utf16[i + 1] << 8)
        h = (31 * h + unit) & 0xFFFFFFFF
    if h >= 0x80000000:
        h -= 0x100000000
    return h


def _java_double_hash(value):
    if math.isnan(value):
        bits = 0x7ff8000000000000
    else:
        bits = struct.unpack('>Q', struct.pack('>d', value))[0]
    h = (bits ^ (bits >> 32)) & 0xFFFFFFFF
    if h >= 0x80000000:
        h -= 0x100000000
    return h


def _java_objects_hash(name, price, quantity):
    h = 1
    h = (31 * h + _java_string_hash(name)) & 0xFFFFFFFF
    h = (31 * h + _java_double_hash(price)) & 0xFFFFFFFF
    h = (31 * h + quantity) & 0xFFFFFFFF
    if h >= 0x80000000:
        h -= 0x100000000
    return h


def _java_double_to_string(value):
    if math.isnan(value):
        return "NaN"
    if value == float('inf'):
        return "Infinity"
    if value == float('-inf'):
        return "-Infinity"
    if value == 0.0:
        if math.copysign(1.0, value) < 0:
            return "-0.0"
        return "0.0"

    sign = ""
    if value < 0:
        sign = "-"
        value = -value

    s = repr(value)
    d = Decimal(s)
    _, digits, exponent = d.as_tuple()
    digit_str = ''.join(str(digit) for digit in digits)

    stripped = digit_str.rstrip('0')
    if stripped == '':
        stripped = '0'
    removed = len(digit_str) - len(stripped)
    digit_str = stripped
    exponent += removed

    first_exp = len(digit_str) + exponent - 1

    if first_exp < -3 or first_exp >= 7:
        mantissa = digit_str[0]
        if len(digit_str) > 1:
            mantissa += "." + digit_str[1:]
        else:
            mantissa += ".0"
        return sign + mantissa + "E" + str(first_exp)
    else:
        if first_exp >= 0:
            int_len = first_exp + 1
            if int_len >= len(digit_str):
                integer_part = digit_str + "0" * (int_len - len(digit_str))
                frac_part = ""
            else:
                integer_part = digit_str[:int_len]
                frac_part = digit_str[int_len:]
            if frac_part == "":
                return sign + integer_part + ".0"
            return sign + integer_part + "." + frac_part
        else:
            zeros = "0" * (-first_exp - 1)
            return sign + "0." + zeros + digit_str


class StockPortfolioTracker:
    class Stock:
        def __init__(self, name, price, quantity):
            self._name = name
            self._price = price
            self._quantity = quantity

        def getName(self):
            return self._name

        def getPrice(self):
            return self._price

        def getQuantity(self):
            return self._quantity

        def setQuantity(self, quantity):
            self._quantity = quantity

        def equals(self, other):
            if self is other:
                return True
            if other is None or type(self) != type(other):
                return False
            return (self._name == other._name and
                    _double_equals(self._price, other._price) and
                    self._quantity == other._quantity)

        def hashCode(self):
            return _java_objects_hash(self._name, self._price, self._quantity)

        def toString(self):
            return (self._name + ": " + str(self._quantity) + " shares at $" +
                    _java_double_to_string(self._price) + " each")

        def __eq__(self, other):
            return self.equals(other)

        def __hash__(self):
            return self.hashCode()

        def __str__(self):
            return self.toString()

    def __init__(self, initialCashBalance):
        self._initialCashBalance = initialCashBalance
        self._cashBalance = initialCashBalance
        self._portfolio = []

    def addStock(self, stock):
        for s in self._portfolio:
            if s.getName() == stock.getName() and s.getPrice() == stock.getPrice():
                s.setQuantity(s.getQuantity() + stock.getQuantity())
                return
        self._portfolio.append(stock)

    def removeStock(self, stock):
        for i, s in enumerate(self._portfolio):
            if s.getName() == stock.getName() and s.getPrice() == stock.getPrice():
                if s.getQuantity() >= stock.getQuantity():
                    s.setQuantity(s.getQuantity() - stock.getQuantity())
                    if s.getQuantity() == 0:
                        del self._portfolio[i]
                    return True
        return False

    def buyStock(self, stock):
        cost = stock.getPrice() * stock.getQuantity()
        if self._cashBalance >= cost:
            self.addStock(stock)
            self._cashBalance -= cost
            return True
        return False

    def sellStock(self, stock):
        revenue = stock.getPrice() * stock.getQuantity()
        if self.removeStock(stock):
            self._cashBalance += revenue
            return True
        return False

    def getPortfolio(self):
        return list(self._portfolio)

    def getCashBalance(self):
        return self._cashBalance

    def calculatePortfolioValue(self):
        totalValue = 0.0
        for stock in self._portfolio:
            totalValue += stock.getPrice() * stock.getQuantity()
        return totalValue

    def getPortfolioSummary(self):
        summary = ""
        for stock in self._portfolio:
            summary += stock.toString() + "\n"
        summary += "Total Value: $" + _java_double_to_string(self.calculatePortfolioValue()) + "\n"
        return summary