class Warehouse:
    def __init__(self):
        self.inventory_ = {}
        self.orders_ = {}

    def add_product(self, product_id, name, quantity):
        product = self.inventory_.get(product_id)
        if not product:
            if product is None:
                product = {}
                self.inventory_[product_id] = product
            product["name"] = name
            product["quantity"] = str(quantity)
        else:
            current_quantity = int(product.setdefault("quantity", ""))
            product["quantity"] = str(current_quantity + quantity)

    def update_product_quantity(self, product_id, quantity):
        product = self.inventory_.get(product_id)
        if product is not None:
            current_quantity = int(product.setdefault("quantity", ""))
            product["quantity"] = str(current_quantity + quantity)

    def get_product_quantity(self, product_id):
        product = self.inventory_.get(product_id)
        if product is not None:
            return int(product["quantity"])
        return 0

    def create_order(self, order_id, product_id, quantity):
        available_quantity = self.get_product_quantity(product_id)
        if available_quantity >= quantity:
            self.update_product_quantity(product_id, -quantity)
            self.orders_[order_id] = {
                "product_id": str(product_id),
                "quantity": str(quantity),
                "status": "Shipped"
            }
            return True
        return False

    def change_order_status(self, order_id, status):
        order = self.orders_.get(order_id)
        if order is not None:
            order["status"] = status
            return True
        return False

    def track_order(self, order_id):
        order = self.orders_.get(order_id)
        if order is not None:
            return order["status"]
        return ""

    def orders(self):
        return self.orders_

    def inventory(self):
        return self.inventory_