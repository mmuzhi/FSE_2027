class Warehouse:
    def __init__(self):
        self._inventory = {}
        self._orders = {}

    def add_product(self, product_id, name, quantity):
        product = self._inventory.get(product_id)
        if product is None:
            self._inventory[product_id] = {
                "name": name,
                "quantity": str(quantity),
            }
        else:
            current_quantity = int(product["quantity"])
            product["quantity"] = str(current_quantity + quantity)

    def update_product_quantity(self, product_id, quantity):
        product = self._inventory.get(product_id)
        if product is not None:
            current_quantity = int(product["quantity"])
            product["quantity"] = str(current_quantity + quantity)

    def get_product_quantity(self, product_id):
        product = self._inventory.get(product_id)
        if product is not None:
            return int(product["quantity"])
        return False  # mirrors C++ `return false;` converted to int 0

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
        order = self._orders.get(order_id)
        if order is not None:
            order["status"] = status
            return True
        return False

    def track_order(self, order_id):
        order = self._orders.get(order_id)
        if order is not None:
            return order["status"]
        return ""

    def orders(self):
        return self._orders

    def inventory(self):
        return self._inventory