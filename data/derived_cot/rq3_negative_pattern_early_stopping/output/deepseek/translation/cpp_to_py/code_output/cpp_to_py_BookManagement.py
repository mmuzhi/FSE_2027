class BookManagement:
    def __init__(self):
        self._inventory = {}

    def add_book(self, title: str, quantity: int = 1) -> None:
        self._inventory[title] = self._inventory.get(title, 0) + quantity

    def remove_book(self, title: str, quantity: int) -> None:
        current = self._inventory.get(title, 0)
        if current < quantity:
            raise RuntimeError("Insufficient quantity or book not found")
        new_quantity = current - quantity
        if new_quantity == 0:
            del self._inventory[title]
        else:
            self._inventory[title] = new_quantity

    def view_inventory(self):
        """Return a copy of the inventory dictionary."""
        return self._inventory.copy()

    def view_book_quantity(self, title: str) -> int:
        return self._inventory.get(title, 0)