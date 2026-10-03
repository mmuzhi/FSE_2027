class Order:
    def __init__(self):
        self.menu = []                # list of dicts
        self.selectedDishes = []      # list of dicts
        self.sales = {}               # dict mapping dish name to multiplier

    def addDish(self, dish):
        if dish is None:
            return False
        if "dish" not in dish or "price" not in dish or "count" not in dish:
            return False

        for menuDish in self.menu:
            if dish["dish"] == menuDish["dish"]:
                dish_count = dish["count"]          # assume int, as in Java
                menu_count = menuDish["count"]
                if menu_count < dish_count:
                    return False
                else:
                    menuDish["count"] = menu_count - dish_count
                    self.selectedDishes.append(dish)
                    return True
        return False

    def calculateTotal(self):
        total = 0.0
        for dish in self.selectedDishes:
            dish_name = dish["dish"]
            price = dish["price"]                 # assume float
            count = dish["count"]                 # assume int
            sale = self.sales.get(dish_name, 1.0)
            total += price * count * sale
        return total

    def checkout(self):
        if not self.selectedDishes:
            return False
        total = self.calculateTotal()
        self.selectedDishes.clear()
        return total