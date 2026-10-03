import math


def _double_compare(a, b):
    if math.isnan(a) and math.isnan(b):
        return 0
    if math.isnan(a):
        return 1
    if math.isnan(b):
        return -1
    if a == 0.0 and b == 0.0:
        a_positive = math.copysign(1.0, a) > 0
        b_positive = math.copysign(1.0, b) > 0
        if a_positive != b_positive:
            return 1 if a_positive else -1
        return 0
    if a < b:
        return -1
    if a > b:
        return 1
    return 0


class StockPortfolioTracker:
    def __init__(self, initial_cash_balance):
        self._initial_cash_balance = initial_cash_balance
        self._cash_balance = initial_cash_balance
        self._portfolio = []

    def add_stock(self, stock):
        for s in self._portfolio:
            if s.name == stock.name and s.price == stock.price:
                s.quantity = s.quantity + stock.quantity
                return
        self._portfolio.append(stock)

    def remove_stock(self, stock):
        for s in self._portfolio:
            if s.name == stock.name and s.price == stock.price:
                if s.quantity >= stock.quantity:
                    s.quantity = s.quantity - stock.quantity
                    if s.quantity == 0:
                        self._portfolio.remove(s)
                    return True
        return False

    def buy_stock(self, stock):
        cost = stock.price * stock.quantity
        if self._cash_balance >= cost:
            self.add_stock(stock)
            self._cash_balance -= cost
            return True
        return False

    def sell_stock(self, stock):
        revenue = stock.price * stock.quantity
        if self.remove_stock(stock):
            self._cash_balance += revenue
            return True
        return False

    def get_portfolio(self):
        return list(self._portfolio)

    def get_cash_balance(self):
        return self._cash_balance

    def calculate_portfolio_value(self):
        total_value = 0.0
        for stock in self._portfolio:
            total_value += stock.price * stock.quantity
        return total_value

    def get_portfolio_summary(self):
        summary = ""
        for stock in self._portfolio:
            summary += str(stock) + "\n"
        summary += "Total Value: $" + str(self.calculate_portfolio_value()) + "\n"
        return summary

    class Stock:
        def __init__(self, name, price, quantity):
            self._name = name
            self._price = price
            self._quantity = quantity

        @property
        def name(self):
            return self._name

        @property
        def price(self):
            return self._price

        @property
        def quantity(self):
            return self._quantity

        @quantity.setter
        def quantity(self, value):
            self._quantity = value

        def __eq__(self, obj):
            if self is obj:
                return True
            if obj is None or type(self) is not type(obj):
                return False
            stock = obj
            return (_double_compare(stock._price, self._price) == 0 and
                    self._quantity == stock._quantity and
                    self._name == stock._name)

        def __hash__(self):
            if math.isnan(self._price):
                price_key = '__nan__'
            else:
                price_key = self._price
            return hash((self._name, price_key, self._quantity))

        def __str__(self):
            return self._name + ": " + str(self._quantity) + " shares at $" + str(self._price) + " each"