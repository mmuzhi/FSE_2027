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
        newQuantity = self.inventory[title] - quantity
        if newQuantity == 0:
            del self.inventory[title]
        else:
            self.inventory[title] = newQuantity

    def viewInventory(self):
        return dict(self.inventory)

    def viewBookQuantity(self, title):
        return self.inventory.get(title, 0)