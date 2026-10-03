import types
from typing import Dict, Optional

class Warehouse:
    def __init__(self):
        self._inventory: Dict[int, Dict[str, str]] = {}
        self._orders: Dict[int, Dict[str, str]] = {}

    def add_product(self, product_id: int, name: str, quantity: int) -> None:
        if product_id in self._inventory:
            current_quantity = int(self._inventory[product_id]["quantity"])
            new_quantity = current_quantity + quantity
            self._inventory[product_id]["quantity"] = str(new_quantity)
        else:
            self._inventory[product_id] = {"name": name, "quantity": str(quantity)}

    def update_product_quantity(self, product_id: int, quantity: int) -> None:
        if product_id in self._inventory:
            current_quantity = int(self._inventory[product_id]["quantity"])
            new_quantity = current_quantity + quantity
            self._inventory[product_id]["quantity"] = str(new_quantity)

    def get_product_quantity(self, product_id: int) -> int:
        return int(self._inventory[product_id]["quantity"]) if product_id in self._inventory else 0

    def create_order(self, order_id: int, product_id: int, quantity: int) -> bool:
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

    def change_order_status(self, order_id: int, status: str) -> bool:
        if order_id in self._orders:
            self._orders[order_id]["status"] = status
            return True
        return False

    def track_order(self, order_id: int) -> str:
        return self._orders[order_id]["status"] if order_id in self._orders else ""

    def inventory(self) -> Dict[int, Dict[str, str]]:
        return types.MappingProxyType(self._inventory)

    def orders(self) -> Dict[int, Dict[str, str]]:
        return types.MappingProxyType(self._orders)