from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Union


class Product:
    def __init__(self, price: float, quantity: int) -> None:
        self.price = price
        self.quantity = quantity


def _format_price(value: float) -> str:
    # Java's String.format("%.2f") applies HALF_UP rounding to the exact double value.
    return str(Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


class VendingMachine:
    def __init__(self) -> None:
        # Python dicts preserve insertion order (LinkedHashMap equivalent);
        # `inventory` and `balance` are directly readable/assignable,
        # covering the getter/setter pairs.
        self.inventory: Dict[str, Product] = {}
        self.balance: float = 0.0

    def add_item(self, item_name: str, price: float, quantity: int) -> None:
        if not self.restock_item(item_name, quantity):
            self.inventory[item_name] = Product(price, quantity)

    def insert_coin(self, amount: float) -> float:
        self.balance += amount
        return self.balance

    def purchase_item(self, item_name: str) -> Union[float, bool]:
        if item_name in self.inventory:
            item = self.inventory[item_name]
            if item.quantity > 0 and self.balance >= item.price:
                self.balance -= item.price
                item.quantity -= 1
                return self.balance
            else:
                return False
        else:
            return False

    def restock_item(self, item_name: str, quantity: int) -> bool:
        if item_name in self.inventory:
            item = self.inventory[item_name]
            item.quantity += quantity
            return True
        else:
            return False

    def display_items(self) -> Union[str, bool]:
        if not self.inventory:
            return False
        else:
            lines = [
                "{} - ${} [{}]".format(
                    name, _format_price(item.price), item.quantity
                )
                for name, item in self.inventory.items()
            ]
            return "\n".join(lines).strip()