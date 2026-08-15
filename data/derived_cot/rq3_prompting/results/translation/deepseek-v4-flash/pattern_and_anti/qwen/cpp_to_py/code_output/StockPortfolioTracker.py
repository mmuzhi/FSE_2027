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
        self.portfolio: List[Stock] = []
        self.cash_balance = cash_balance

    def add_stock(self, stock: Stock) -> None:
        for pf in self.portfolio:
            if pf.name == stock.name:
                pf.quantity += stock.quantity
                return
        self.portfolio.append(Stock(stock.name, stock.price, stock.quantity))

    def remove_stock(self, stock: Stock) -> bool:
        for i, pf in enumerate(self.portfolio):
            if pf.name == stock.name and pf.quantity >= stock.quantity:
                pf.quantity -= stock.quantity
                if pf.quantity == 0:
                    del self.portfolio[i]
                return True
        return False

    def buy_stock(self, stock: Stock) -> bool:
        cost = stock.price * stock.quantity
        if cost > self.cash_balance:
            return False
        else:
            self.add_stock(stock)
            self.cash_balance -= cost
            return True

    def sell_stock(self, stock: Stock) -> bool:
        if not self.remove_stock(stock):
            return False
        self.cash_balance += stock.price * stock.quantity
        return True

    def calculate_portfolio_value(self) -> float:
        total_value = self.cash_balance
        for stock in self.portfolio:
            total_value += stock.price * stock.quantity
        return total_value

    def get_portfolio_summary(self) -> Tuple[float, List[StockSummary]]:
        summary: List[StockSummary] = []
        for stock in self.portfolio:
            summary.append(StockSummary(stock.name, self.get_stock_value(stock)))
        return (self.calculate_portfolio_value(), summary)

    def get_stock_value(self, stock: Stock) -> float:
        return stock.price * stock.quantity

    def get_portfolio(self) -> List[Stock]:
        return self.portfolio

    def get_cash_balance(self) -> float:
        return self.cash_balance

    def set_portfolio(self, p: List[Stock]) -> None:
        self.portfolio = [Stock(s.name, s.price, s.quantity) for s in p]