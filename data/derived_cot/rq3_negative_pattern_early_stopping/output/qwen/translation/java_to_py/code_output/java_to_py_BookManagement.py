class BookManagement:
    def __init__(self):
        self.inventory = {}

    def add_book(self, title: str, quantity: int) -> None:
        if title in self.inventory:
            self.inventory[title] += quantity
        else:
            self.inventory[title] = quantity

    def remove_book(self, title: str, quantity: int) -> None:
        current_quantity = self.inventory.get(title, 0)
        if current_quantity < quantity:
            raise ValueError("Invalid operation")
        new_quantity = current_quantity - quantity
        if new_quantity == 0:
            del self.inventory[title]
        else:
            self.inventory[title] = new_quantity

    def view_inventory(self) -> dict:
        return self.inventory.copy()

    def view_book_quantity(self, title: str) -> int:
        return self.inventory.get(title, 0)