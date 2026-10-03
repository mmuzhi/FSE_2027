class Product:
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


class VendingMachine:
    def __init__(self):
        self.inventory = {}
        self.balance = 0.0

    def addItem(self, itemName, price, quantity):
        if not self.restockItem(itemName, quantity):
            self.inventory[itemName] = Product(price, quantity)

    def insertCoin(self, amount):
        self.balance += amount
        return self.balance

    def purchaseItem(self, itemName):
        if itemName in self.inventory:
            item = self.inventory[itemName]
            if item.getQuantity() > 0 and self.balance >= item.getPrice():
                self.balance -= item.getPrice()
                item.setQuantity(item.getQuantity() - 1)
                return self.balance
            else:
                return False
        else:
            return False

    def restockItem(self, itemName, quantity):
        if itemName in self.inventory:
            item = self.inventory[itemName]
            item.setQuantity(item.getQuantity() + quantity)
            return True
        else:
            return False

    def displayItems(self):
        if not self.inventory:
            return False
        else:
            items = []
            for name, item in self.inventory.items():
                items.append(f"{name} - ${item.getPrice():.2f} [{item.getQuantity()}]")
            return "\n".join(items)

    def getInventory(self):
        return self.inventory

    def setInventory(self, inventory):
        self.inventory = inventory

    def getBalance(self):
        return self.balance

    def setBalance(self, balance):
        self.balance = balance