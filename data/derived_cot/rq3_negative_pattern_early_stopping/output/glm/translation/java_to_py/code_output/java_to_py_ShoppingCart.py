import math


class ShoppingCart:

    def __init__(self):
        self._items = {}

    def addItem(self, item, price, quantity):
        if item in self._items:
            existing_item = self._items[item]
            existing_item.setPrice(price)
            existing_item.setQuantity(existing_item.getQuantity() + quantity)
        else:
            self._items[item] = Item(price, quantity)

    def removeItem(self, item, quantity):
        if item in self._items:
            existing_item = self._items[item]
            new_quantity = existing_item.getQuantity() - quantity
            if new_quantity <= 0:
                del self._items[item]
            else:
                existing_item.setQuantity(new_quantity)

    def viewItems(self):
        return dict(self._items)

    def totalPrice(self):
        total = 0.0
        for item in self._items.values():
            total += item.getPrice() * item.getQuantity()
        return total


class Item:

    def __init__(self, price, quantity):
        self._price = price
        self._quantity = quantity

    def getPrice(self):
        return self._price

    def setPrice(self, price):
        self._price = price

    def getQuantity(self):
        return self._quantity

    def setQuantity(self, quantity):
        self._quantity = quantity

    def __eq__(self, other):
        if self is other:
            return True
        if type(self) is not type(other):
            return False
        return (_double_compare(self._price, other._price) == 0
                and self._quantity == other._quantity)

    def __hash__(self):
        return hash((_double_key(self._price), self._quantity))


def _double_compare(a, b):
    """Replicates Java's Double.compare semantics."""
    if math.isnan(a) and math.isnan(b):
        return 0
    if math.isnan(a):
        return 1
    if math.isnan(b):
        return -1
    if a == b:
        if a == 0.0:
            sa = math.copysign(1, a)
            sb = math.copysign(1, b)
            if sa < sb:
                return -1
            elif sa > sb:
                return 1
            return 0
        return 0
    return -1 if a < b else 1


def _double_key(d):
    """Returns a hashable key consistent with _double_compare for use in __hash__."""
    if math.isnan(d):
        return ('NaN',)
    if d == 0.0:
        return ('zero', math.copysign(1, d))
    return d