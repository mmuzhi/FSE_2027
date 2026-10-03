class PromoType:
    FidelityPromo = 0
    BulkItemPromo = 1
    LargeOrderPromo = 2
    NoPromo = 3

class DiscountStrategy:
    def __init__(self, customer, cart, promo=PromoType.NoPromo):
        self.customer = customer
        self.cart = cart
        self.promo = promo

    def total(self):
        total = 0.0
        for item in self.cart:
            total += item['quantity'] * item['price']
        return total

    def due(self):
        return self.total() - self.promotion(self)

    def promotion(self, order):
        if self.promo == PromoType.FidelityPromo:
            return self.fidelity_discount()
        elif self.promo == PromoType.BulkItemPromo:
            return self.bulk_item_discount()
        elif self.promo == PromoType.LargeOrderPromo:
            return self.large_order_discount()
        else:
            return 0.0

    def fidelity_discount(self):
        fidelity = self.customer['fidelity']
        return 0.05 * self.total() if fidelity >= 1000.0 else 0.0

    def bulk_item_discount(self):
        discount = 0.0
        for item in self.cart:
            if item['quantity'] >= 20:
                discount += item['quantity'] * item['price'] * 0.1
        return discount

    def large_order_discount(self):
        num_items = len(self.cart)
        return 0.07 * self.total() if num_items >= 10 else 0.0