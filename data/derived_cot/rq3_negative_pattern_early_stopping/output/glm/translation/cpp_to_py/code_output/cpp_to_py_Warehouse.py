class Warehouse:
    def __init__(self):
        self._inventory = {}
        self._orders = {}

    def add_product(self, product_id, name, quantity):
        if product_id not in self._inventory:
            self._inventory[product_id] = {
                "name": name,
                "quantity": str(quantity)
            }
        else:
            current_quantity = int(self._inventory[product_id]["quantity"])
            self._inventory[product_id]["quantity"] = str(current_quantity + quantity)

    def update_product_quantity(self, product_id, quantity):
        if product_id in self._inventory:
            current_quantity = int(self._inventory[product_id]["quantity"])
            self._inventory[product_id]["quantity"] = str(current_quantity + quantity)

    def get_product_quantity(self, product_id):
        if product_id in self._inventory:
            return int(self._inventory[product_id]["quantity"])
        return 0  # C++ returns false which implicitly converts to int 0

    def create_order(self, order_id, product_id, quantity):
        available_quantity = self.get_product_quantity(product_id)
        if available_quantity >= quantity:
            self.update_product_quantity(product_id, -quantity)
            self._orders[order_id] = {
                "product_id": str(product_id),
                "quantity": str(quantity),
                "status": "Shipped"
            }
            return True
        return False

    def change_order_status(self, order_id, status):
        if order_id in self._orders:
            self._orders[order_id]["status"] = status
            return True
        return False

    def track_order(self, order_id):
        if order_id in self._orders:
            return self._orders[order_id]["status"]
        return ""

    @property
    def orders(self):
        return self._orders

    @property
    def inventory(self):
        return self._inventory