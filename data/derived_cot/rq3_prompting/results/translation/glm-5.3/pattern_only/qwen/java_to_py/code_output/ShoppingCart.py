import math


class ShoppingCart:
    class Item:
        __slots__ = ("price", "quantity")

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
            if type(self) is not type(other):  # covers null (None) and other classes
                return False
            if self.quantity != other.quantity:
                return False
            p1, p2 = self.price, other.price
            # Double.compare: NaN == NaN, +0.0 != -0.0
            if math.isnan(p1) and math.isnan(p2):
                return True
            if p1 == p2:
                if p1 == 0.0:
                    return math.copysign(1.0, p1) == math.copysign(1.0, p2)
                return True
            return False

        def __hash__(self):
            return hash((self.quantity, self.price))

    def __init__(self):
        self.items = {}

    def addItem(self, item, price, quantity):
        if item in self.items:
            existing = self.items[item]
            existing.price = price
            existing.quantity = existing.quantity + quantity
        else:
            self.items[item] = ShoppingCart.Item(price, quantity)

    def removeItem(self, item, quantity):
        if item in self.items:
            existing = self.items[item]
            new_quantity = existing.quantity - quantity
            if new_quantity <= 0:
                del self.items[item]
            else:
                existing.quantity = new_quantity

    def viewItems(self):
        return dict(self.items)  # shallow copy, same as new HashMap<>(items)

    def totalPrice(self):
        total = 0.0
        for item in self.items.values():
            total += item.price * item.quantity
        return total