class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, item: str, price: float, quantity: int = 1):
        self.items[item] = (price, quantity)

    def remove_item(self, item: str, quantity: int = 1):
        if item in self.items:
            price, current_quantity = self.items[item]
            current_quantity -= quantity
            if current_quantity <= 0:
                del self.items[item]
            else:
                self.items[item] = (price, current_quantity)

    def view_items(self):
        return dict(self.items)

    def total_price(self):
        total = 0.0
        for price, quantity in self.items.values():
            total += price * quantity
        return total