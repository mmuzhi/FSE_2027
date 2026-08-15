class BookManagement:
    def __init__(self):
        self.inventory = {}

    def add_book(self, title, quantity):
        if title in self.inventory:
            self.inventory[title] += quantity
        else:
            self.inventory[title] = quantity

    def remove_book(self, title, quantity):
        if title not in self.inventory or self.inventory[title] < quantity:
            raise Exception("Invalid operation")
        new_quantity = self.inventory[title] - quantity
        if new_quantity == 0:
            del self.inventory[title]
        else:
            self.inventory[title] = new_quantity

    def view_inventory(self):
        return dict(self.inventory)

    def view_book_quantity(self, title):
        return self.inventory.get(title, 0)