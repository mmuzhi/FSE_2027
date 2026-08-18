class StockPortfolioTracker:
    def __init__(self, initial_cash_balance):
        self.initial_cash_balance = initial_cash_balance
        self.cash_balance = initial_cash_balance
        self.portfolio = []

    def add_stock(self, stock):
        for s in self.portfolio:
            if s.name == stock.name and s.price == stock.price:
                s.quantity += stock.quantity
                return
        self.portfolio.append(stock)

    def remove_stock(self, stock):
        for s in self.portfolio:
            if s.name == stock.name and s.price == stock.price:
                if s.quantity >= stock.quantity:
                    s.quantity -= stock.quantity
                    if s.quantity == 0:
                        self.portfolio.remove(s)
                    return True
        return False

    def buy_stock(self, stock):
        cost = stock.price * stock.quantity
        if self.cash_balance >= cost:
            self.add_stock(stock)
            self.cash_balance -= cost
            return True
        return False

    def sell_stock(self, stock):
        revenue = stock.price * stock.quantity
        if self.remove_stock(stock):
            self.cash_balance += revenue
            return True
        return False

    def get_portfolio(self):
        return list(self.portfolio)

    def get_cash_balance(self):
        return self.cash_balance

    def calculate_portfolio_value(self):
        total_value = 0.0
        for stock in self.portfolio:
            total_value += stock.price * stock.quantity
        return total_value

    def get_portfolio_summary(self):
        parts = []
        for stock in self.portfolio:
            parts.append(str(stock))
            parts.append("\n")
        parts.append(f"Total Value: ${self.calculate_portfolio_value()}\n")
        return "".join(parts)

    class Stock:
        __slots__ = ("name", "price", "quantity")

        def __init__(self, name, price, quantity):
            self.name = name
            self.price = price
            self.quantity = quantity

        def get_name(self):
            return self.name

        def get_price(self):
            return self.price

        def get_quantity(self):
            return self.quantity

        def set_quantity(self, quantity):
            self.quantity = quantity

        def __eq__(self, other):
            if self is other:
                return True
            if type(other) is not type(self):
                return False
            return (self.price == other.price
                    and self.quantity == other.quantity
                    and self.name == other.name)

        def __hash__(self):
            return hash((self.name, self.price, self.quantity))

        def __str__(self):
            return f"{self.name}: {self.quantity} shares at ${self.price} each"

        __repr__ = __str__