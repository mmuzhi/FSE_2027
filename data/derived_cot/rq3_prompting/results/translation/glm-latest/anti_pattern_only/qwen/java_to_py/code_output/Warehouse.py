class Product:
    def __init__(self, name: str, quantity: int) -> None:
        self.name = name
        self.quantity = quantity

    def add_quantity(self, quantity: int) -> None:
        self.quantity += quantity

    def get_quantity(self) -> int:
        return self.quantity


class Order:
    def __init__(self, product_id: int, quantity: int, status: str) -> None:
        self.product_id = product_id
        self.quantity = quantity
        self.status = status

    def get_status(self) -> str:
        return self.status

    def set_status(self, status: str) -> None:
        self.status = status


class Warehouse:
    def __init__(self) -> None:
        self.inventory: dict[int, Product] = {}
        self.orders: dict[int, Order] = {}

    def add_product(self, product_id: int, name: str, quantity: int) -> None:
        if product_id in self.inventory:
            self.inventory[product_id].add_quantity(quantity)
        else:
            self.inventory[product_id] = Product(name, quantity)

    def update_product_quantity(self, product_id: int, quantity: int) -> None:
        if product_id in self.inventory:
            self.inventory[product_id].add_quantity(quantity)

    def get_product_quantity(self, product_id: int) -> int:
        if product_id in self.inventory:
            return self.inventory[product_id].get_quantity()
        return -1

    def create_order(self, order_id: int, product_id: int, quantity: int) -> bool:
        if product_id in self.inventory and self.inventory[product_id].get_quantity() >= quantity:
            self.inventory[product_id].add_quantity(-quantity)
            self.orders[order_id] = Order(product_id, quantity, "Shipped")
            return True
        return False

    def change_order_status(self, order_id: int, status: str) -> bool:
        if order_id in self.orders:
            self.orders[order_id].set_status(status)
            return True
        return False

    def track_order(self, order_id: int) -> str | None:
        if order_id in self.orders:
            return self.orders[order_id].get_status()
        return None