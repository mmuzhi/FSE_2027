import copy


class VendingMachine:
    def __init__(self):
        self.inventory_ = {}
        self.balance_ = 0.0

    def add_item(self, item_name, price, quantity):
        if not self.restock_item(item_name, quantity):
            self.inventory_[item_name] = {"price": price, "quantity": float(quantity)}

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
        return 0.0  # C++ `return false;` converts to double 0.0

    def restock_item(self, item_name, quantity):
        if item_name in self.inventory_:
            self.inventory_[item_name]["quantity"] += float(quantity)
            return True
        return False

    def display_items(self):
        if not self.inventory_:
            return "false"
        # C++ ostream default formatting == %g (6 significant digits, no trailing ".0")
        return "\n".join(
            "{} - ${} [{}]".format(
                name,
                "%.6g" % item["price"],
                "%.6g" % item["quantity"],
            )
            for name, item in self.inventory_.items()
        )

    def inventory(self):
        return copy.deepcopy(self.inventory_)  # C++ returns by value

    def set_inventory(self, x):
        self.inventory_ = copy.deepcopy(x)  # C++ copies the map argument

    def set_balance(self, y):
        self.balance_ = y