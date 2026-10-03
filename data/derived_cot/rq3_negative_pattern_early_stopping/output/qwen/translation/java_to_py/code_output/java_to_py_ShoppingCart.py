class ShoppingCart:
    def __init__(self):
        self.items = {}

    def addItem(self, item, price, quantity):
        if item in self.items:
            existing_item = self.items[item]
            existing_item.setPrice(price)
            existing_item.setQuantity(existing_item.getQuantity() + quantity)
        else:
            self.items[item] = Item(price, quantity)

    def removeItem(self, item, quantity):
        if item in self.items:
            existing_item = self.items[item]
            new_quantity = existing_item.getQuantity() - quantity
            if new_quantity <= 0:
                del self.items[item]
            else:
                existing_item.setQuantity(new_quantity)

    def viewItems(self):
        return self.items.copy()

    def totalPrice(self):
        total = 0.0
        for item in self.items.values():
            total += item.getPrice() * item.getQuantity()
        return total

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

# Example usage:
# cart = ShoppingCart()
# cart.addItem("apple", 1.5, 10)
# cart.addItem("banana", 0.5, 5)
# print(cart.viewItems())
# cart.removeItem("apple", 5)
# print(cart.totalPrice())