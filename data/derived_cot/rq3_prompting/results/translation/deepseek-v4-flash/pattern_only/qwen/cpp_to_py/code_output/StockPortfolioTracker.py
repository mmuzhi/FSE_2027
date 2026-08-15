from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class Stock:
    name: str
    price: float
    quantity: int


@dataclass(frozen=True)
class StockSummary:
    name: str
    value: float


class _PortfolioView:
    def __init__(self, portfolio: List[Stock]):
        self._portfolio = portfolio

    def __len__(self) -> int:
        return len(self._portfolio)

    def __getitem__(self, index):
        return self._portfolio[index]

    def __iter__(self):
        return iter(self._portfolio)

    def __eq__(self, other):
        if isinstance(other, _PortfolioView):
            return self._portfolio == other._portfolio
        if isinstance(other, list):
            return list(self._portfolio) == other
        return NotImplemented

    def __repr__(self) -> str:
        return repr(list(self._portfolio))


class StockPortfolioTracker:
    def __init__(self, cash_balance: float):
        self.portfolio: List[Stock] = []
        self.cash_balance = cash_balance
        self._portfolio_view = _PortfolioView(self.portfolio)

    def add_stock(self, stock: Stock) -> None:
        for i, pf in enumerate(self.portfolio):
            if pf.name == stock.name:
                self.portfolio[i] = Stock(pf.name, pf.price, pf.quantity + stock.quantity)
                return
        self.portfolio.append(Stock(stock.name, stock.price, stock.quantity))

    def remove_stock(self, stock: Stock) -> bool:
        for i, pf in enumerate(self.portfolio):
            if pf.name == stock.name and pf.quantity >= stock.quantity:
                new_quantity = pf.quantity - stock.quantity
                if new_quantity == 0:
                    del self.portfolio[i]
                else:
                    self.portfolio[i] = Stock(pf.name, pf.price, new_quantity)
                return True
        return False

    def buy_stock(self, stock: Stock) -> bool:
        cost = stock.price * stock.quantity
        if cost > self.cash_balance:
            return False
        self.add_stock(stock)
        self.cash_balance -= cost
        return True

    def sell_stock(self, stock: Stock) -> bool:
        if not self.remove_stock(stock):
            return False
        self.cash_balance += stock.price * stock.quantity
        return True

    def calculate_portfolio_value(self) -> float:
        total = self.cash_balance
        for stock in self.portfolio:
            total += stock.price * stock.quantity
        return total

    def get_portfolio_summary(self) -> Tuple[float, List[StockSummary]]:
        summary = [StockSummary(stock.name, self.get_stock_value(stock)) for stock in self.portfolio]
        return (self.calculate_portfolio_value(), summary)

    def get_stock_value(self, stock: Stock) -> float:
        return stock.price * stock.quantity

    def get_portfolio(self) -> _PortfolioView:
        return self._portfolio_view

    def get_cash_balance(self) -> float:
        return self.cash_balance

    def set_portfolio(self, p: List[Stock]) -> None:
        self.portfolio[:] = [Stock(s.name, s.price, s.quantity) for s in p]