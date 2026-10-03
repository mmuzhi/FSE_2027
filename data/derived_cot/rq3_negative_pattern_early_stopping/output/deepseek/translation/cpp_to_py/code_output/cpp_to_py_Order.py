class Dish:
    def __init__(self, dish: str, price: float, count: int):
        self.dish = dish
        self.price = price
        self.count = count


class Order:
    def __init__(self):
        self.menu = []               # list of Dish objects
        self.selected_dishes = []    # list of Dish objects
        self.sales = {}              # dict: dish name -> float multiplier

    def add_dish(self, dish: Dish) -> bool:
        for menu_dish in self.menu:
            if dish.dish == menu_dish.dish:
                if menu_dish.count < dish.count:
                    return False     # not enough in stock
                else:
                    menu_dish.count -= dish.count
                    break
        else:
            pass

        self.selected_dishes.append(Dish(dish.dish, dish.price, dish.count))
        return True

    def calculate_total(self) -> float:
        total = 0.0
        for dish in self.selected_dishes:
            multiplier = self.sales.get(dish.dish)
            if multiplier is not None:   # equivalent to finding a key in unordered_map
                total += dish.price * dish.count * multiplier
        return total

    def checkout(self) -> float:
        if not self.selected_dishes:     # empty list
            return 0.0
        total = self.calculate_total()
        self.selected_dishes.clear()
        return total