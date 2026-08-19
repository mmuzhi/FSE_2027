from typing import Protocol


class DiscountStrategy:
    class Promotion(Protocol):
        def __call__(self, order: "DiscountStrategy") -> float: ...

    def __init__(self, customer: "Customer", cart: "Cart", promotion=None):
        self.customer = customer
        self.cart = cart
        self._promotion = promotion
        self.total()

    def total(self) -> float:
        self._total = sum(p.quantity * p.price for p in self.cart.products)
        return self._total

    def due(self) -> float:
        discount = 0 if self._promotion is None else self._promotion(self)
        return self._total - discount

    def promotion(self, order) -> float:
        return 0 if self._promotion is None else self._promotion(self)

    class Customer:
        def __init__(self, name: str, fidelity: int):
            self.name = name
            self.fidelity = fidelity

    class Cart:
        def __init__(self, *products):
            self.products = list(products)

        def add_product(self, product):
            self.products.append(product)

    class Product:
        def __init__(self, name: str, quantity: int, price: float):
            self.name = name
            self.quantity = quantity
            self.price = price


# Assigned after class definition so they stay plain functions (never bind as methods).
DiscountStrategy.FIDELITY_PROMO = lambda order: (
    order.total() * 0.05 if order.customer.fidelity >= 1000 else 0
)

DiscountStrategy.BULK_ITEM_PROMO = lambda order: sum(
    (item.quantity * item.price * 0.1
     for item in order.cart.products if item.quantity >= 20),
    0.0,
)

DiscountStrategy.LARGE_ORDER_PROMO = lambda order: (
    order.total() * 0.07 if len(order.cart.products) >= 10 else 0
)