class Dish:
    def __init__(self, dish, price, count):
        self.dish = dish
        self.price = price
        self.count = count


class Order:
    def __init__(self):
        self.menu = []
        self.selected_dishes = []
        self.sales = {}  # Key: dish name, Value: discount factor

    def add_dish(self, dish):
        # Search for dish in menu
        for menu_dish in self.menu:
            if dish.dish == menu_dish.dish:
                if menu_dish.count < dish.count:
                    return False
                menu_dish.count -= dish.count
                break
        # Add dish to selected_dishes
        self.selected_dishes.append(Dish(dish.dish, dish.price, dish.count))
        return True

    def calculate_total(self):
        total = 0.0
        for selected_dish in self.selected_dishes:
            # Get discount factor, default to 1.0 if not found
            discount = self.sales.get(selected_dish.dish, 1.0)
            total += selected_dish.price * selected_dish.count * discount
        return total

    def checkout(self):
        if not self.selected_dishes:
            return 0.0
        total = self.calculate_total()
        self.selected_dishes.clear()
        return total