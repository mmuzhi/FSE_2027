import math


def _double_equals(a, b):
    # Mimics Java's Double.compare(a, b) == 0
    if math.isnan(a) and math.isnan(b):
        return True
    if a == b:
        if a == 0.0:
            return math.copysign(1.0, a) == math.copysign(1.0, b)
        return True
    return False


class ShoppingCart:
    class Item:
        def __init__(self, price, quantity):
            self.price = price
            self.quantity = quantity

        def getPrice(self):
            return self.price

        def setPrice(self, price):
            self.price = price

        def getQuantity(self):
            return self.quantity

        def setQuantity(self, quantity):
            self.quantity = quantity

        def __eq__(self, other):
            if self is other:
                return True
            if other is None or type(self) is not type(other):
                return False
            return _double_equals(self.price, other.price) and self.quantity == other.quantity

        def __hash__(self):
            return hash((self.price, self.quantity))

    def __init__(self):
        self.items = {}

    def addItem(self, item, price, quantity):
        if item in self.items:
            existing = self.items[item]
            existing.setPrice(price)
            existing.setQuantity(existing.getQuantity() + quantity)
        else:
            self.items[item] = ShoppingCart.Item(price, quantity)

    def removeItem(self, item, quantity):
        if item in self.items:
            existing = self.items[item]
            newQuantity = existing.getQuantity() - quantity
            if newQuantity <= 0:
                del self.items[item]
            else:
                existing.setQuantity(newQuantity)

    def viewItems(self):
        return dict(self.items)

    def totalPrice(self):
        total = 0.0
        for item in self.items.values():
            total += item.getPrice() * item.getQuantity()
        return total