class Product:
    def __init__(self, price, quantity):
        self.price = price
        self.quantity = quantity

    def get_price(self):
        return self.price

    def set_price(self, price):
        self.price = price

    def get_quantity(self):
        return self.quantity

    def set_quantity(self, quantity):
        self.quantity = quantity


class VendingMachine:
    def __init__(self):
        self.inventory = {}
        self.balance = 0.0

    def addItem(self, itemName, price, quantity):
        if itemName in self.inventory:
            self.inventory[itemName].set_quantity(self.inventory[itemName].get_quantity() + quantity)
        else:
            self.inventory[itemName] = Product(price, quantity)

    def insertCoin(self, amount):
        self.balance += amount
        return self.balance

    def purchaseItem(self, itemName):
        if itemName in self.inventory:
            item = self.inventory[itemName]
            if item.get_quantity() > 0 and self.balance >= item.get_price():
                self.balance -= item.get_price()
                item.set_quantity(item.get_quantity() - 1)
                return self.balance
        return False

    def restockItem(self, itemName, quantity):
        if itemName in self.inventory:
            self.inventory[itemName].set_quantity(self.inventory[itemName].get_quantity() + quantity)
            return True
        return False

    def displayItems(self):
        if not self.inventory:
            return False
        output = []
        for itemName, product in self.inventory.items():
            output.append(f"{itemName} - ${product.get_price():.2f} [{product.get_quantity()}]")
        return "\n".join(output)

    def get_inventory(self):
        return self.inventory

    def set_inventory(self, inventory):
        self.inventory = inventory

    def get_balance(self):
        return self.balance

    def set_balance(self, balance):
        self.balance = balance