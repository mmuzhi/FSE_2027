class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, item, price, quantity=1):
        self.items[item] = (price, quantity)

    def remove_item(self, item, quantity=1):
        if item in self.items:
            current_price, current_quantity = self.items[item]
            new_quantity = current_quantity - quantity
            if new_quantity <= 0:
                del self.items[item]
            else:
                self.items[item] = (current_price, new_quantity)

    def view_items(self):
        return self.items

    def total_price(self):
        return sum(price * quantity for price, quantity in self.items.values())