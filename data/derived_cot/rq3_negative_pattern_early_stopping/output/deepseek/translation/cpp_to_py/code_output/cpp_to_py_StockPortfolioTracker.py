from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Stock:
    name: str
    price: float
    quantity: int

    def __eq__(self, other):
        if not isinstance(other, Stock):
            return NotImplemented
        return (self.name == other.name and
                self.price == other.price and
                self.quantity == other.quantity)

@dataclass
class StockSummary:
    name: str
    value: float

    def __eq__(self, other):
        if not isinstance(other, StockSummary):
            return NotImplemented
        return self.name == other.name and self.value == other.value


class StockPortfolioTracker:
    def __init__(self, cash_balance: float):
        self._cash_balance = cash_balance
        self._portfolio: List[Stock] = []

    def add_stock(self, stock: Stock) -> None:
        stock_copy = Stock(name=stock.name, price=stock.price, quantity=stock.quantity)
        for pf in self._portfolio:
            if pf.name == stock_copy.name:
                pf.quantity += stock_copy.quantity
                return
        self._portfolio.append(stock_copy)

    def remove_stock(self, stock: Stock) -> bool:
        for i, pf in enumerate(self._portfolio):
            if pf.name == stock.name and pf.quantity >= stock.quantity:
                pf.quantity -= stock.quantity
                if pf.quantity == 0:
                    self._portfolio.pop(i)
                return True
        return False

    def buy_stock(self, stock: Stock) -> bool:
        cost = stock.price * stock.quantity
        if cost > self._cash_balance:
            return False
        self.add_stock(stock)          # add_stock makes a copy
        self._cash_balance -= cost
        return True

    def sell_stock(self, stock: Stock) -> bool:
        if not self.remove_stock(stock):
            return False
        self._cash_balance += stock.price * stock.quantity
        return True

    def calculate_portfolio_value(self) -> float:
        total = self._cash_balance
        for s in self._portfolio:
            total += s.price * s.quantity
        return total

    def get_portfolio_summary(self) -> Tuple[float, List[StockSummary]]:
        summary = [StockSummary(name=s.name, value=self.get_stock_value(s))
                   for s in self._portfolio]
        return (self.calculate_portfolio_value(), summary)

    def get_stock_value(self, stock: Stock) -> float:
        return stock.price * stock.quantity

    def get_portfolio(self) -> List[Stock]:
        return list(self._portfolio)

    def get_cash_balance(self) -> float:
        return self._cash_balance

    def set_portfolio(self, portfolio: List[Stock]) -> None:
        self._portfolio = [Stock(name=s.name, price=s.price, quantity=s.quantity)
                           for s in portfolio]