class DiscountStrategy:
    FidelityPromo = 0
    BulkItemPromo = 1
    LargeOrderPromo = 2
    NoPromo = 3

    def __init__(self, customer, cart, promo=NoPromo):
        self.customer_ = customer
        self.cart_ = cart
        self.promo_ = promo

    def total(self):
        total = 0.0
        for item in self.cart_:
            total += item["quantity"] * item["price"]
        return total

    def due(self):
        return self.total() - self.promotion(self)

    def promotion(self, order):
        if self.promo_ == DiscountStrategy.FidelityPromo:
            return self.fidelity_discount()
        elif self.promo_ == DiscountStrategy.BulkItemPromo:
            return self.bulk_item_discount()
        elif self.promo_ == DiscountStrategy.LargeOrderPromo:
            return self.large_order_discount()
        else:
            return 0.0

    def fidelity_discount(self):
        total = 0.0
        fidelity = self.customer_["fidelity"]
        if fidelity >= 1000.0:
            total = 0.05 * self.total()
        return total

    def bulk_item_discount(self):
        discount = 0.0
        for item in self.cart_:
            if item["quantity"] >= 20:
                discount += item["quantity"] * item["price"] * 0.1
        return discount

    def large_order_discount(self):
        num_items = len(self.cart_)
        discount = 0.0
        if num_items >= 10:
            discount = 0.07 * self.total()
        return discount