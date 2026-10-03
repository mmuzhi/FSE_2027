from enum import Enum
from typing import Dict, List


class PromoType(Enum):
    FidelityPromo = 1
    BulkItemPromo = 2
    LargeOrderPromo = 3
    NoPromo = 4


class DiscountStrategy:
    def __init__(
        self,
        customer: Dict[str, float],
        cart: List[Dict[str, float]],
        promo: PromoType = PromoType.NoPromo,
    ):
        self.customer_ = customer
        self.cart_ = cart
        self.promo_ = promo

    def total(self) -> float:
        total = 0.0
        for item in self.cart_:
            total += item["quantity"] * item["price"]
        return total

    def due(self) -> float:
        return self.total() - self.promotion(self)

    def promotion(self, order: "DiscountStrategy") -> float:
        if self.promo_ == PromoType.FidelityPromo:
            return self.fidelity_discount()
        elif self.promo_ == PromoType.BulkItemPromo:
            return self.bulk_item_discount()
        elif self.promo_ == PromoType.LargeOrderPromo:
            return self.large_order_discount()
        else:
            return 0.0

    def fidelity_discount(self) -> float:
        total = 0.0
        fidelity = self.customer_["fidelity"]
        if fidelity >= 1000.0:
            total = 0.05 * self.total()
        return total

    def bulk_item_discount(self) -> float:
        discount = 0.0
        for item in self.cart_:
            if item["quantity"] >= 20:
                discount += item["quantity"] * item["price"] * 0.1
        return discount

    def large_order_discount(self) -> float:
        num_items = len(self.cart_)
        discount = 0.0
        if num_items >= 10:
            discount = 0.07 * self.total()
        return discount