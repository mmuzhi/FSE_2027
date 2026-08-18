class Warehouse:
    class _Product:
        def __init__(self, name, quantity):
            self.name = name
            self.quantity = quantity

        def add_quantity(self, quantity):
            self.quantity += quantity

        def get_quantity(self):
            return self.quantity

    class _Order:
        def __init__(self, product_id, quantity, status):
            self.product_id = product_id
            self.quantity = quantity
            self.status = status

        def get_status(self):
            return self.status

        def set_status(self, status):
            self.status = status

    def __init__(self):
        self.inventory = {}
        self.orders = {}

    def add_product(self, product_id, name, quantity):
        if product_id in self.inventory:
            self.inventory[product_id].add_quantity(quantity)
        else:
            self.inventory[product_id] = self._Product(name, quantity)

    def update_product_quantity(self, product_id, quantity):
        if product_id in self.inventory:
            self.inventory[product_id].add_quantity(quantity)

    def get_product_quantity(self, product_id):
        if product_id in self.inventory:
            return self.inventory[product_id].get_quantity()
        else:
            return -1

    def create_order(self, order_id, product_id, quantity):
        if product_id in self.inventory and self.inventory[product_id].get_quantity() >= quantity:
            self.inventory[product_id].add_quantity(-quantity)
            self.orders[order_id] = self._Order(product_id, quantity, "Shipped")
            return True
        else:
            return False

    def change_order_status(self, order_id, status):
        if order_id in self.orders:
            self.orders[order_id].set_status(status)
            return True
        else:
            return False

    def track_order(self, order_id):
        if order_id in self.orders:
            return self.orders[order_id].get_status()
        else:
            return None