class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, item: str, price: float, quantity: int = 1):
        self.items[item] = (price, quantity)

    def remove_item(self, item: str, quantity: int = 1):
        if item in self.items:
            new_qty = self.items[item][1] - quantity
            if new_qty <= 0:
                del self.items[item]
            else:
                self.items[item] = (self.items[item][0], new_qty)

    def view_items(self):
        return dict(self.items)

    def total_price(self):
        total = 0.0
        for price, qty in self.items.values():
            total += price * qty
        return total