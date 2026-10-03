class Warehouse:
    class Product:
        def __init__(self, name, quantity):
            self.name = name
            self.quantity = quantity

        def addQuantity(self, quantity):
            self.quantity += quantity

        def getQuantity(self):
            return self.quantity

    class Order:
        def __init__(self, productId, quantity, status):
            self.productId = productId
            self.quantity = quantity
            self.status = status

        def getStatus(self):
            return self.status

        def setStatus(self, status):
            self.status = status

    def __init__(self):
        self.inventory = {}
        self.orders = {}

    def addProduct(self, productId, name, quantity):
        if productId in self.inventory:
            self.inventory[productId].addQuantity(quantity)
        else:
            self.inventory[productId] = self.Product(name, quantity)

    def updateProductQuantity(self, productId, quantity):
        if productId in self.inventory:
            self.inventory[productId].addQuantity(quantity)

    def getProductQuantity(self, productId):
        if productId in self.inventory:
            return self.inventory[productId].getQuantity()
        else:
            return -1

    def createOrder(self, orderId, productId, quantity):
        if productId in self.inventory and self.inventory[productId].getQuantity() >= quantity:
            self.inventory[productId].addQuantity(-quantity)
            self.orders[orderId] = self.Order(productId, quantity, "Shipped")
            return True
        else:
            return False

    def changeOrderStatus(self, orderId, status):
        if orderId in self.orders:
            self.orders[orderId].setStatus(status)
            return True
        else:
            return False

    def trackOrder(self, orderId):
        if orderId in self.orders:
            return self.orders[orderId].getStatus()
        else:
            return None