from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Stock:
    name: str
    price: float
    quantity: int


@dataclass
class StockSummary:
    name: str
    value: float


class StockPortfolioTracker:
    def __init__(self, cash_balance: float):
        self._portfolio: List[Stock] = []
        self._cash_balance: float = cash_balance

    def add_stock(self, stock: Stock) -> None:
        for pf in self._portfolio:
            if pf.name == stock.name:
                pf.quantity += stock.quantity
                return
        self._portfolio.append(stock)

    def remove_stock(self, stock: Stock) -> bool:
        for i, pf in enumerate(self._portfolio):
            if pf.name == stock.name and pf.quantity >= stock.quantity:
                pf.quantity -= stock.quantity
                if pf.quantity == 0:
                    self._portfolio.pop(i)
                return True
        return False

    def buy_stock(self, stock: Stock) -> bool:
        if stock.price * stock.quantity > self._cash_balance:
            return False
        else:
            self.add_stock(stock)
            self._cash_balance -= stock.price * stock.quantity
            return True

    def sell_stock(self, stock: Stock) -> bool:
        if not self.remove_stock(stock):
            return False
        self._cash_balance += stock.price * stock.quantity
        return True

    def calculate_portfolio_value(self) -> float:
        total_value = self._cash_balance
        for stock in self._portfolio:
            total_value += stock.price * stock.quantity
        return total_value

    def get_portfolio_summary(self) -> Tuple[float, List[StockSummary]]:
        summary = []
        for stock in self._portfolio:
            summary.append(StockSummary(stock.name, self.get_stock_value(stock)))
        return (self.calculate_portfolio_value(), summary)

    def get_stock_value(self, stock: Stock) -> float:
        return stock.price * stock.quantity

    def get_portfolio(self) -> List[Stock]:
        return self._portfolio

    def get_cash_balance(self) -> float:
        return self._cash_balance

    def set_portfolio(self, portfolio: List[Stock]) -> None:
        self._portfolio = list(portfolio)