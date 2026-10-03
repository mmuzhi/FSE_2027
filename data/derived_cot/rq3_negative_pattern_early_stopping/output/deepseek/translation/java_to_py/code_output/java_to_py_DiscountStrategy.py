from typing import List, Callable, Optional


class DiscountStrategy:
    Promotion = Callable[['DiscountStrategy'], float]

    @staticmethod
    def _fidelity_promo(order: 'DiscountStrategy') -> float:
        if order.customer.get_fidelity() >= 1000:
            return order.total() * 0.05
        return 0.0

    @staticmethod
    def _bulk_item_promo(order: 'DiscountStrategy') -> float:
        discount = 0.0
        for item in order.cart.get_products():
            if item.get_quantity() >= 20:
                discount += item.get_quantity() * item.get_price() * 0.1
        return discount

    @staticmethod
    def _large_order_promo(order: 'DiscountStrategy') -> float:
        if len(order.cart.get_products()) >= 10:
            return order.total() * 0.07
        return 0.0

    FIDELITY_PROMO = _fidelity_promo
    BULK_ITEM_PROMO = _bulk_item_promo
    LARGE_ORDER_PROMO = _large_order_promo

    def __init__(self, customer: 'Customer', cart: 'Cart', promotion: Optional['Promotion']):
        self.customer = customer
        self.cart = cart
        self.promotion = promotion
        self.total = self._compute_total()

    def _compute_total(self) -> float:
        total = sum(p.get_quantity() * p.get_price() for p in self.cart.get_products())
        self.total = total
        return total

    def total(self) -> float:
        return self._compute_total()

    def due(self) -> float:
        discount = 0.0 if self.promotion is None else self.promotion(self)
        return self.total - discount

    def promotion(self, order: 'DiscountStrategy') -> float:
        return 0.0 if self.promotion is None else self.promotion(order)


    class Customer:
        def __init__(self, name: str, fidelity: int):
            self._name = name
            self._fidelity = fidelity

        def get_name(self) -> str:
            return self._name

        def get_fidelity(self) -> int:
            return self._fidelity

    class Cart:
        def __init__(self, *products: 'Product'):
            self._products: List['Product'] = []
            for product in products:
                self._products.append(product)

        def add_product(self, product: 'Product') -> None:
            self._products.append(product)

        def get_products(self) -> List['Product']:
            return self._products

    class Product:
        def __init__(self, name: str, quantity: int, price: float):
            self._name = name
            self._quantity = quantity
            self._price = price

        def get_name(self) -> str:
            return self._name

        def get_quantity(self) -> int:
            return self._quantity

        def get_price(self) -> float:
            return self._price