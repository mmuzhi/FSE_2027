from typing import List, Dict

class Dish:
    def __init__(self, dish: str = "", price: float = 0.0, count: int = 0):
        self.dish = dish
        self.price = price
        self.count = count

class Order:
    def __init__(self):
        self.menu: List[Dish] = []
        self.selected_dishes: List[Dish] = []
        self.sales: Dict[str, float] = {}

    def add_dish(self, dish: Dish) -> bool:
        for menu_dish in self.menu:
            if dish.dish == menu_dish.dish:
                if menu_dish.count < dish.count:
                    return False
                menu_dish.count -= dish.count
                break
        self.selected_dishes.append(dish)
        return True

    def calculate_total(self) -> float:
        total = 0.0
        for dish in self.selected_dishes:
            if dish.dish in self.sales:
                total += dish.price * dish.count * self.sales[dish.dish]
        return total

    def checkout(self) -> float:
        if not self.selected_dishes:
            return 0.0
        total = self.calculate_total()
        self.selected_dishes.clear()
        return total