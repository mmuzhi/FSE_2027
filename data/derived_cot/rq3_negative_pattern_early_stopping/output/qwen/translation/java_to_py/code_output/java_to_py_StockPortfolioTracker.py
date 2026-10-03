class StockPortfolioTracker:
    class Stock:
        def __init__(self, name, price, quantity):
            self.name = name
            self.price = price
            self.quantity = quantity

        @property
        def name(self):
            return self._name

        @property
        def price(self):
            return self._price

        @property
        def quantity(self):
            return self._quantity

        def set_quantity(self, quantity):
            self._quantity = quantity

        def __eq__(self, other):
            if not isinstance(other, Stock):
                return False
            return (self.name == other.name and 
                    self.price == other.price and 
                    self.quantity == other.quantity)

        def __hash__(self):
            return hash((self.name, self.price, self.quantity))

        def __str__(self):
            return f"{self.name}: {self.quantity} shares at ${self.price} each"

    def __init__(self, initial_cash_balance):
        self.initial_cash_balance = initial_cash_balance
        self.cash_balance = initial_cash_balance
        self.portfolio = []

    def add_stock(self, stock):
        for existing_stock in self.portfolio:
            if (existing_stock.name == stock.name and 
                existing_stock.price == stock.price):
                existing_stock.quantity += stock.quantity
                return
        self.portfolio.append(stock)

    def remove_stock(self, stock):
        for idx, existing_stock in enumerate(self.portfolio):
            if (existing_stock.name == stock.name and 
                existing_stock.price == stock.price):
                if existing_stock.quantity >= stock.quantity:
                    existing_stock.quantity -= stock.quantity
                    if existing_stock.quantity == 0:
                        del self.portfolio[idx]
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
        return [stock for stock in self.portfolio]

    def get_cash_balance(self):
        return self.cash_balance

    def calculate_portfolio_value(self):
        return sum(stock.price * stock.quantity for stock in self.portfolio)

    def get_portfolio_summary(self):
        summary = []
        for stock in self.portfolio:
            summary.append(str(stock))
        summary.append(f"Total Value: ${self.calculate_portfolio_value()}")
        return "\n".join(summary)