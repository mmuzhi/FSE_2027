class BookManagement:
    def __init__(self):
        self.inventory = {}

    def addBook(self, title, quantity):
        if title in self.inventory:
            self.inventory[title] = self.inventory[title] + quantity
        else:
            self.inventory[title] = quantity

    def removeBook(self, title, quantity):
        if title not in self.inventory or self.inventory[title] < quantity:
            raise Exception("Invalid operation")
        new_quantity = self.inventory[title] - quantity
        if new_quantity == 0:
            del self.inventory[title]
        else:
            self.inventory[title] = new_quantity

    def viewInventory(self):
        return dict(self.inventory)

    def viewBookQuantity(self, title):
        return self.inventory.get(title, 0)