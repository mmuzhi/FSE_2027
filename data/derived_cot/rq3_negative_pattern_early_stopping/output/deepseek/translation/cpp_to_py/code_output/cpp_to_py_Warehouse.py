from types import MappingProxyType

class Warehouse:
    def __init__(self):
        self._inventory = {}
        self._orders = {}

    def add_product(self, product_id: int, name: str, quantity: int) -> None:
        if product_id not in self._inventory:
            self._inventory[product_id] = {}
        product = self._inventory[product_id]
        if not product:  # newly created empty dict
            product["name"] = name
            product["quantity"] = str(quantity)
        else:
            current = int(product["quantity"])
            product["quantity"] = str(current + quantity)

    def update_product_quantity(self, product_id: int, quantity: int) -> None:
        if product_id in self._inventory:
            current = int(self._inventory[product_id]["quantity"])
            self._inventory[product_id]["quantity"] = str(current + quantity)

    def get_product_quantity(self, product_id: int) -> int:
        if product_id in self._inventory:
            return int(self._inventory[product_id]["quantity"])
        return 0

    def create_order(self, order_id: int, product_id: int, quantity: int) -> bool:
        available = self.get_product_quantity(product_id)
        if available >= quantity:
            self.update_product_quantity(product_id, -quantity)
            self._orders[order_id] = {
                "product_id": str(product_id),
                "quantity": str(quantity),
                "status": "Shipped"
            }
            return True
        return False

    def change_order_status(self, order_id: int, status: str) -> bool:
        if order_id in self._orders:
            self._orders[order_id]["status"] = status
            return True
        return False

    def track_order(self, order_id: int) -> str:
        if order_id in self._orders:
            return self._orders[order_id]["status"]
        return ""

    @property
    def orders(self):
        return MappingProxyType(self._orders)

    @property
    def inventory(self):
        return MappingProxyType(self._inventory)