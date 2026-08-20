class Warehouse:
    def __init__(self):
        self._inventory = {}
        self._orders = {}

    def add_product(self, product_id, name, quantity):
        # operator[] semantics: create an empty record if the product is absent
        product = self._inventory.setdefault(product_id, {})
        if not product:
            product["name"] = name
            product["quantity"] = str(quantity)
        else:
            current_quantity = int(product["quantity"])
            product["quantity"] = str(current_quantity + quantity)

    def update_product_quantity(self, product_id, quantity):
        if product_id in self._inventory:
            product = self._inventory[product_id]
            current_quantity = int(product["quantity"])
            product["quantity"] = str(current_quantity + quantity)

    def get_product_quantity(self, product_id):
        if product_id in self._inventory:
            return int(self._inventory[product_id]["quantity"])
        return False  # false converts to 0 in the C++ int return

    def create_order(self, order_id, product_id, quantity):
        available_quantity = self.get_product_quantity(product_id)
        if available_quantity >= quantity:
            self.update_product_quantity(product_id, -quantity)
            self._orders[order_id] = {
                "product_id": str(product_id),
                "quantity": str(quantity),
                "status": "Shipped",
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

    def orders(self):
        return self._orders

    def inventory(self):
        return self._inventory