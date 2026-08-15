class Order:
    def __init__(self):
        self.menu = []
        self.selectedDishes = []
        self.sales = {}

    def addDish(self, dish):
        if dish is None or "dish" not in dish or "price" not in dish or "count" not in dish:
            return False

        for menu_dish in self.menu:
            if dish["dish"] == menu_dish["dish"]:
                dish_count = int(dish["count"])
                menu_dish_count = int(menu_dish["count"])

                if menu_dish_count < dish_count:
                    return False
                else:
                    menu_dish["count"] = menu_dish_count - dish_count
                    self.selectedDishes.append(dish)
                    return True
        return False

    def calculateTotal(self):
        total = 0.0
        for dish in self.selectedDishes:
            dish_name = dish["dish"]
            price = float(dish["price"])
            count = int(dish["count"])
            sale = self.sales.get(dish_name, 1.0)
            total += price * count * sale
        return total

    def checkout(self):
        if not self.selectedDishes:
            return False
        total = self.calculateTotal()
        self.selectedDishes.clear()
        return total