from decimal import Decimal, ROUND_HALF_UP


class _FalseType:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __bool__(self):
        return False

    def __repr__(self):
        return "false"

    def __str__(self):
        return "false"

    def __eq__(self, other):
        if isinstance(other, _FalseType):
            return True
        if other is False:
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(False)


_FALSE = _FalseType()


class Balance:
    def __init__(self, value):
        self._value = float(value)

    @property
    def value(self):
        return self._value

    def __float__(self):
        return self._value

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return repr(self._value)

    def __format__(self, spec):
        return format(self._value, spec)

    def __eq__(self, other):
        if isinstance(other, bool):
            return False
        if isinstance(other, Balance):
            return self._value == other._value
        if isinstance(other, (int, float)):
            return self._value == other
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __hash__(self):
        return hash(self._value)


def _format_name(name):
    return "null" if name is None else str(name)


def _format_price(price):
    return Decimal.from_float(float(price)).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP
    )


class VendingMachine:
    class Product:
        def __init__(self, price, quantity):
            self._price = float(price)
            self._quantity = quantity

        def getPrice(self):
            return self._price

        def setPrice(self, price):
            self._price = float(price)

        def getQuantity(self):
            return self._quantity

        def setQuantity(self, quantity):
            self._quantity = quantity

    def __init__(self):
        self.inventory = {}
        self.balance = 0.0

    def addItem(self, itemName, price, quantity):
        if not self.restockItem(itemName, quantity):
            self.inventory[itemName] = self.Product(price, quantity)

    def insertCoin(self, amount):
        self.balance += amount
        return self.balance

    def purchaseItem(self, itemName):
        if itemName in self.inventory:
            item = self.inventory[itemName]
            if item.getQuantity() > 0 and self.balance >= item.getPrice():
                self.balance -= item.getPrice()
                item.setQuantity(item.getQuantity() - 1)
                return Balance(self.balance)
            else:
                return _FALSE
        else:
            return _FALSE

    def restockItem(self, itemName, quantity):
        if itemName in self.inventory:
            item = self.inventory[itemName]
            item.setQuantity(item.getQuantity() + quantity)
            return True
        else:
            return False

    def displayItems(self):
        if not self.inventory:
            return _FALSE
        lines = []
        for name, item in self.inventory.items():
            lines.append(
                f"{_format_name(name)} - ${_format_price(item.getPrice())} [{item.getQuantity()}]"
            )
        return "\n".join(lines)

    def getInventory(self):
        return self.inventory

    def setInventory(self, inventory):
        self.inventory = inventory

    def getBalance(self):
        return self.balance

    def setBalance(self, balance):
        self.balance = float(balance)