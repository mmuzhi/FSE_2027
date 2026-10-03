class ShoppingCart:
    class Item:
        def __init__(self, price: float, quantity: int):
            self._price = price
            self._quantity = quantity

        def getPrice(self) -> float:
            return self._price

        def setPrice(self, price: float):
            self._price = price

        def getQuantity(self) -> int:
            return self._quantity

        def setQuantity(self, quantity: int):
            self._quantity = quantity

        def __eq__(self, other):
            if self is other:
                return True
            if other is None or type(other) != type(self):
                return False
            return (self._price == other._price) and (self._quantity == other._quantity)

        def __hash__(self):
            return hash((self._price, self._quantity))

    def __init__(self):
        self.items = {}

    def addItem(self, item: str, price: float, quantity: int):
        if item in self.items:
            existing = self.items[item]
            existing.setPrice(price)
            existing.setQuantity(existing.getQuantity() + quantity)
        else:
            self.items[item] = ShoppingCart.Item(price, quantity)

    def removeItem(self, item: str, quantity: int):
        if item in self.items:
            existing = self.items[item]
            new_quantity = existing.getQuantity() - quantity
            if new_quantity <= 0:
                del self.items[item]
            else:
                existing.setQuantity(new_quantity)

    def viewItems(self):
        return self.items.copy()

    def totalPrice(self) -> float:
        total = 0.0
        for it in self.items.values():
            total += it.getPrice() * it.getQuantity()
        return total