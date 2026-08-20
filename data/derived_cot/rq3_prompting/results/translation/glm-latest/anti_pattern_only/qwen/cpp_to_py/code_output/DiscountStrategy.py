from enum import Enum, auto


class DiscountStrategy:
    class PromoType(Enum):
        FidelityPromo = auto()
        BulkItemPromo = auto()
        LargeOrderPromo = auto()
        NoPromo = auto()

    def __init__(self, customer, cart, promo=PromoType.NoPromo):
        # C++ copies the map and the vector of maps into members;
        # mirror that value semantics so later mutations of the
        # caller's objects don't affect this instance.
        self._customer = dict(customer)
        self._cart = [dict(item) for item in cart]
        self._promo = promo

    def total(self):
        total = 0.0
        for item in self._cart:
            total += item["quantity"] * item["price"]
        return total

    def due(self):
        return self.total() - self.promotion(self)

    def promotion(self, order):
        if self._promo is self.PromoType.FidelityPromo:
            return self._fidelity_discount()
        elif self._promo is self.PromoType.BulkItemPromo:
            return self._bulk_item_discount()
        elif self._promo is self.PromoType.LargeOrderPromo:
            return self._large_order_discount()
        else:
            return 0.0

    def _fidelity_discount(self):
        total = 0.0
        fidelity = self._customer["fidelity"]
        if fidelity >= 1000.0:
            total = 0.05 * self.total()
        return total

    def _bulk_item_discount(self):
        discount = 0.0
        for item in self._cart:
            if item["quantity"] >= 20:
                discount += item["quantity"] * item["price"] * 0.1
        return discount

    def _large_order_discount(self):
        num_items = len(self._cart)
        discount = 0.0
        if num_items >= 10:
            discount = 0.07 * self.total()
        return discount