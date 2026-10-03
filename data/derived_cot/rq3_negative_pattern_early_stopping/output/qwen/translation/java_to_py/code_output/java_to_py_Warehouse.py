class Warehouse:
    def __init__(self):
        self.inventory = {}
        self.orders = {}

    def add_product(self, product_id, name, quantity):
        if product_id in self.inventory:
            self.inventory[product_id].add_quantity(quantity)
        else:
            self.inventory[product_id] = Product(name, quantity)

    def update_product_quantity(self, product_id, quantity):
        if product_id in self.inventory:
            self.inventory[product_id].add_quantity(quantity)

    def get_product_quantity(self, product_id):
        return self.inventory[product_id].quantity if product_id in self.inventory else -1

    def create_order(self, order_id, product_id, quantity):
        if product_id in self.inventory and self.inventory[product_id].quantity >= quantity:
            self.inventory[product_id].add_quantity(-quantity)
            self.orders[order_id] = Order(product_id, quantity, "Shipped")
            return True
        return False

    def change_order_status(self, order_id, status):
        if order_id in self.orders:
            self.orders[order_id].status = status
            return True
        return False

    def track_order(self, order_id):
        return self.orders[order_id].status if order_id in self.orders else None


class Product:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def add_quantity(self, quantity):
        self.quantity += quantity


class Order:
    def __init__(self, product_id, quantity, status):
        self.product_id = product_id
        self.quantity = quantity
        self.status = status