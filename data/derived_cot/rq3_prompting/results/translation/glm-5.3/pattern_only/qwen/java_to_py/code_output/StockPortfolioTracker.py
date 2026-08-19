class StockPortfolioTracker:

    class Stock:
        __slots__ = ("name", "price", "quantity")

        def __init__(self, name, price, quantity):
            self.name = name
            self.price = price
            self.quantity = quantity

        def getName(self):
            return self.name

        def getPrice(self):
            return self.price

        def getQuantity(self):
            return self.quantity

        def setQuantity(self, quantity):
            self.quantity = quantity

        def __eq__(self, other):
            if self is other:
                return True
            if other is None or type(other) is not type(self):
                return False
            return (other.price == self.price and
                    other.quantity == self.quantity and
                    self.name == other.name)

        def __hash__(self):
            return hash((self.name, self.price, self.quantity))

        def __str__(self):
            return f"{self.name}: {self.quantity} shares at ${self.price} each"

        def __repr__(self):
            return self.__str__()

    def __init__(self, initialCashBalance):
        self.initialCashBalance = initialCashBalance
        self.cashBalance = initialCashBalance
        self.portfolio = []

    def addStock(self, stock):
        for s in self.portfolio:
            if s.getName() == stock.getName() and s.getPrice() == stock.getPrice():
                s.setQuantity(s.getQuantity() + stock.getQuantity())
                return
        self.portfolio.append(stock)

    def removeStock(self, stock):
        for s in self.portfolio:
            if s.getName() == stock.getName() and s.getPrice() == stock.getPrice():
                if s.getQuantity() >= stock.getQuantity():
                    s.setQuantity(s.getQuantity() - stock.getQuantity())
                    if s.getQuantity() == 0:
                        self.portfolio.remove(s)
                    return True
        return False

    def buyStock(self, stock):
        cost = stock.getPrice() * stock.getQuantity()
        if self.cashBalance >= cost:
            self.addStock(stock)
            self.cashBalance -= cost
            return True
        return False

    def sellStock(self, stock):
        revenue = stock.getPrice() * stock.getQuantity()
        if self.removeStock(stock):
            self.cashBalance += revenue
            return True
        return False

    def getPortfolio(self):
        return list(self.portfolio)

    def getCashBalance(self):
        return self.cashBalance

    def calculatePortfolioValue(self):
        totalValue = 0.0
        for stock in self.portfolio:
            totalValue += stock.getPrice() * stock.getQuantity()
        return totalValue

    def getPortfolioSummary(self):
        summary = ""
        for stock in self.portfolio:
            summary += str(stock) + "\n"
        summary += "Total Value: $" + str(self.calculatePortfolioValue()) + "\n"
        return summary