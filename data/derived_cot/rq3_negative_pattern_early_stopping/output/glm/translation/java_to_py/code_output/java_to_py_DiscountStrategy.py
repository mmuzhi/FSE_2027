class DiscountStrategy:

    @staticmethod
    def fidelity_promo(order):
        return order.total() * 0.05 if order.customer.get_fidelity() >= 1000 else 0

    @staticmethod
    def bulk_item_promo(order):
        discount = 0
        for item in order.cart.get_products():
            if item.get_quantity() >= 20:
                discount += item.get_quantity() * item.get_price() * 0.1
        return discount

    @staticmethod
    def large_order_promo(order):
        return order.total() * 0.07 if len(order.cart.get_products()) >= 10 else 0

    FIDELITY_PROMO = fidelity_promo
    BULK_ITEM_PROMO = bulk_item_promo
    LARGE_ORDER_PROMO = large_order_promo

    def __init__(self, customer, cart, promotion):
        self.customer = customer
        self.cart = cart
        self._promotion = promotion
        self._total = self.total()

    def total(self):
        self._total = sum(p.get_quantity() * p.get_price() for p in self.cart.get_products())
        return self._total

    def due(self):
        discount = 0 if self._promotion is None else self._promotion(self)
        return self._total - discount

    def promotion(self, order):
        return 0 if self._promotion is None else self._promotion(self)

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
            self.products = list(products)

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