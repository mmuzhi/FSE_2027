class Stock:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def __eq__(self, other):
        if not isinstance(other, Stock):
            return False
        return (self.name == other.name and 
                self.price == other.price and 
                self.quantity == other.quantity)


class StockSummary:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, StockSummary):
            return False
        return (self.name == other.name and 
                self.value == other.value)


class StockPortfolioTracker:
    def __init__(self, cash_balance):
        self.cash_balance = cash_balance
        self.portfolio = []

    def add_stock(self, stock):
        for existing_stock in self.portfolio:
            if existing_stock.name == stock.name:
                existing_stock.quantity += stock.quantity
                return
        self.portfolio.append(stock)

    def remove_stock(self, stock):
        for i, existing_stock in enumerate(self.portfolio):
            if (existing_stock.name == stock.name and 
                existing_stock.quantity >= stock.quantity):
                existing_stock.quantity -= stock.quantity
                if existing_stock.quantity == 0:
                    del self.portfolio[i]
                return True
        return False

    def buy_stock(self, stock):
        if stock.price * stock.quantity > self.cash_balance:
            return False
        self.add_stock(stock)
        self.cash_balance -= stock.price * stock.quantity
        return True

    def sell_stock(self, stock):
        if not self.remove_stock(stock):
            return False
        self.cash_balance += stock.price * stock.quantity
        return True

    def calculate_portfolio_value(self):
        total_value = self.cash_balance
        for stock in self.portfolio:
            total_value += stock.price * stock.quantity
        return total_value

    def get_portfolio_summary(self):
        summary_list = []
        for stock in self.portfolio:
            summary_list.append(StockSummary(stock.name, stock.price * stock.quantity))
        return (self.calculate_portfolio_value(), summary_list)

    def get_stock_value(self, stock):
        return stock.price * stock.quantity

    def get_portfolio(self):
        return self.portfolio

    def get_cash_balance(self):
        return self.cash_balance

    def set_portfolio(self, portfolio):
        self.portfolio = portfolio