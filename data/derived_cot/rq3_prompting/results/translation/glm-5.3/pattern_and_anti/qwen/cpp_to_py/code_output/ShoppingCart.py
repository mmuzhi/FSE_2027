class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, item, price, quantity=1):
        if item in self.items:
            self.items[item] = (price, quantity)
        else:
            self.items[item] = (price, quantity)

    def remove_item(self, item, quantity=1):
        if item in self.items:
            price, qty = self.items[item]
            qty -= quantity
            if qty <= 0:
                del self.items[item]
            else:
                self.items[item] = (price, qty)

    def view_items(self):
        return dict(self.items)

    def total_price(self):
        total = 0.0
        for price, quantity in self.items.values():
            total += price * quantity
        return total