class VendingMachine:
    def __init__(self):
        self._inventory = {}
        self._balance = 0.0

    def add_item(self, item_name: str, price: float, quantity: int) -> None:
        if not self.restock_item(item_name, quantity):
            self._inventory[item_name] = {"price": float(price), "quantity": float(quantity)}

    def insert_coin(self, amount: float) -> float:
        self._balance += amount
        return self._balance

    def purchase_item(self, item_name: str) -> float:
        if item_name in self._inventory:
            item = self._inventory[item_name]
            if item["quantity"] > 0 and self._balance >= item["price"]:
                self._balance -= item["price"]
                item["quantity"] -= 1.0
                return self._balance
        return 0.0

    def restock_item(self, item_name: str, quantity: int) -> bool:
        if item_name in self._inventory:
            self._inventory[item_name]["quantity"] += float(quantity)
            return True
        return False

    def display_items(self) -> str:
        if not self._inventory:
            return "false"
        lines = []
        for name, attr in self._inventory.items():
            price_str = f"{attr['price']:g}"
            qty_str = f"{attr['quantity']:g}"
            lines.append(f"{name} - ${price_str} [{qty_str}]")
        return "\n".join(lines)

    def inventory(self):
        return {k: dict(v) for k, v in self._inventory.items()}

    def set_inventory(self, x):
        self._inventory = {k: dict(v) for k, v in x.items()}

    def set_balance(self, y: float) -> None:
        self._balance = y