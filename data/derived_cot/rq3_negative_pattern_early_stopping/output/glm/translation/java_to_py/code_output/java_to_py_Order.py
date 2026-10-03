class Order:
    def __init__(self):
        self.menu = []
        self.selectedDishes = []
        self.sales = {}

    def addDish(self, dish):
        if dish is None or "dish" not in dish or "price" not in dish or "count" not in dish:
            return False

        for menuDish in self.menu:
            if dish.get("dish") == menuDish.get("dish"):
                dishCount = int(dish.get("count"))
                menuDishCount = int(menuDish.get("count"))

                if menuDishCount < dishCount:
                    return False
                else:
                    menuDish["count"] = menuDishCount - dishCount
                    self.selectedDishes.append(dish)
                    return True

        return False

    def calculateTotal(self):
        total = 0.0
        for dish in self.selectedDishes:
            dishName = dish.get("dish")
            price = float(dish.get("price"))
            count = int(dish.get("count"))
            sale = self.sales.get(dishName, 1.0)
            total += price * count * sale
        return total

    def checkout(self):
        if not self.selectedDishes:
            return False
        total = self.calculateTotal()
        self.selectedDishes.clear()
        return total