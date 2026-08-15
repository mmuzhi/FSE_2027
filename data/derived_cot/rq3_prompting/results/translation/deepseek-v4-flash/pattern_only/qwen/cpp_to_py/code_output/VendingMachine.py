class VendingMachine:
    def __init__(self):
        self.balance_ = 0.0
        self.inventory_ = {}

    def add_item(self, item_name, price, quantity):
        if not self.restock_item(item_name, quantity):
            self.inventory_[item_name] = {"price": float(price), "quantity": float(quantity)}

    def insert_coin(self, amount):
        self.balance_ += amount
        return self.balance_

    def purchase_item(self, item_name):
        if item_name in self.inventory_:
            item = self.inventory_[item_name]
            if item["quantity"] > 0 and self.balance_ >= item["price"]:
                self.balance_ -= item["price"]
                item["quantity"] -= 1
                return self.balance_
        return 0.0

    def restock_item(self, item_name, quantity):
        if item_name in self.inventory_:
            self.inventory_[item_name]["quantity"] += float(quantity)
            return True
        return False

    def display_items(self):
        if not self.inventory_:
            return "false"
        lines = []
        for name, data in self.inventory_.items():
            lines.append(f"{name} - ${format(data['price'], '.6g')} [{format(data['quantity'], '.6g')}]")
        return "\n".join(lines)

    def inventory(self):
        return {k: dict(v) for k, v in self.inventory_.items()}

    def set_inventory(self, x):
        self.inventory_ = {k: dict(v) for k, v in x.items()}

    def set_balance(self, y):
        self.balance_ = float(y)