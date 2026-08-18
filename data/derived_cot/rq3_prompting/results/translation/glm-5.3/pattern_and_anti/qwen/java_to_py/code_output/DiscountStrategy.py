# Promotions: callables serving as the Promotion functional interface
FIDELITY_PROMO = lambda order: (
    order.total() * 0.05 if order.customer.get_fidelity() >= 1000 else 0.0
)


def BULK_ITEM_PROMO(order):
    discount = 0.0
    for item in order.cart.get_products():
        if item.get_quantity() >= 20:
            discount += item.get_quantity() * item.get_price() * 0.1
    return discount


LARGE_ORDER_PROMO = lambda order: (
    order.total() * 0.07 if len(order.cart.get_products()) >= 10 else 0.0
)


class DiscountStrategy:
    def __init__(self, customer, cart, promotion):
        self.customer = customer
        self.cart = cart
        self._promotion = promotion  # field; kept separate from promotion() method
        self._total = self.total()

    def total(self):
        self._total = sum(
            (p.get_quantity() * p.get_price() for p in self.cart.get_products()),
            0.0,
        )
        return self._total

    def due(self):
        discount = 0.0 if self._promotion is None else self._promotion(self)
        return self._total - discount

    def promotion(self, order):
        # parameter is ignored, promotion applied to `self` (as in Java)
        return 0.0 if self._promotion is None else self._promotion(self)


class Customer:
    def __init__(self, name, fidelity):
        self.name = name
        self.fidelity = fidelity

    def get_name(self):
        return self.name

    def get_fidelity(self):
        return self.fidelity


class Cart:
    def __init__(self, *products):
        self.products = []
        for product in products:
            self.products.append(product)

    def add_product(self, product):
        self.products.append(product)

    def get_products(self):
        return self.products


class Product:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price

    def get_name(self):
        return self.name

    def get_quantity(self):
        return self.quantity

    def get_price(self):
        return self.price