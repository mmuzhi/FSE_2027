from enum import IntEnum

class DiscountStrategy:
    class PromoType(IntEnum):
        FidelityPromo = 0
        BulkItemPromo = 1
        LargeOrderPromo = 2
        NoPromo = 3

    def __init__(self, customer, cart, promo=PromoType.NoPromo):
        self.customer_ = dict(customer)
        self.cart_ = [dict(item) for item in cart]
        self.promo_ = promo

    def total(self):
        total = 0.0
        for item in self.cart_:
            total += item["quantity"] * item["price"]
        return total

    def due(self):
        return self.total() - self.promotion(self)

    def promotion(self, order):
        if self.promo_ == self.PromoType.FidelityPromo:
            return self._fidelity_discount()
        elif self.promo_ == self.PromoType.BulkItemPromo:
            return self._bulk_item_discount()
        elif self.promo_ == self.PromoType.LargeOrderPromo:
            return self._large_order_discount()
        else:
            return 0.0

    def _fidelity_discount(self):
        total = 0.0
        fidelity = self.customer_["fidelity"]
        if fidelity >= 1000.0:
            total = 0.05 * self.total()
        return total

    def _bulk_item_discount(self):
        discount = 0.0
        for item in self.cart_:
            if item["quantity"] >= 20:
                discount += item["quantity"] * item["price"] * 0.1
        return discount

    def _large_order_discount(self):
        num_items = len(self.cart_)
        discount = 0.0
        if num_items >= 10:
            discount = 0.07 * self.total()
        return discount