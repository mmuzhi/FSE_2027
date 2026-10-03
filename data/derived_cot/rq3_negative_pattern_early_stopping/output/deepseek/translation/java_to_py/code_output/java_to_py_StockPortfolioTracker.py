from typing import List

class StockPortfolioTracker:
    class Stock:
        def __init__(self, name: str, price: float, quantity: int):
            self.name = name
            self.price = price
            self.quantity = quantity

        def get_name(self) -> str:
            return self.name

        def get_price(self) -> float:
            return self.price

        def get_quantity(self) -> int:
            return self.quantity

        def set_quantity(self, quantity: int) -> None:
            self.quantity = quantity

        def __eq__(self, other) -> bool:
            if self is other:
                return True
            if not isinstance(other, StockPortfolioTracker.Stock):
                return False
            return (self.name == other.name and
                    self.price == other.price and
                    self.quantity == other.quantity)

        def __hash__(self) -> int:
            return hash((self.name, self.price, self.quantity))

        def __str__(self) -> str:
            return f"{self.name}: {self.quantity} shares at ${self.price} each"

    def __init__(self, initial_cash_balance: float):
        self.initial_cash_balance = initial_cash_balance
        self.cash_balance = initial_cash_balance
        self.portfolio: List[StockPortfolioTracker.Stock] = []

    def add_stock(self, stock: Stock) -> None:
        for s in self.portfolio:
            if s.get_name() == stock.get_name() and s.get_price() == stock.get_price():
                s.set_quantity(s.get_quantity() + stock.get_quantity())
                return
        self.portfolio.append(stock)

    def remove_stock(self, stock: Stock) -> bool:
        for s in self.portfolio:
            if s.get_name() == stock.get_name() and s.get_price() == stock.get_price():
                if s.get_quantity() >= stock.get_quantity():
                    s.set_quantity(s.get_quantity() - stock.get_quantity())
                    if s.get_quantity() == 0:
                        self.portfolio.remove(s)
                    return True
        return False

    def buy_stock(self, stock: Stock) -> bool:
        cost = stock.get_price() * stock.get_quantity()
        if self.cash_balance >= cost:
            self.add_stock(stock)
            self.cash_balance -= cost
            return True
        return False

    def sell_stock(self, stock: Stock) -> bool:
        revenue = stock.get_price() * stock.get_quantity()
        if self.remove_stock(stock):
            self.cash_balance += revenue
            return True
        return False

    def get_portfolio(self) -> List[Stock]:
        return list(self.portfolio)

    def get_cash_balance(self) -> float:
        return self.cash_balance

    def calculate_portfolio_value(self) -> float:
        total_value = 0.0
        for stock in self.portfolio:
            total_value += stock.get_price() * stock.get_quantity()
        return total_value

    def get_portfolio_summary(self) -> str:
        summary_lines = [str(stock) for stock in self.portfolio]
        total_val = self.calculate_portfolio_value()
        summary_lines.append(f"Total Value: ${total_val}")
        return "\n".join(summary_lines)