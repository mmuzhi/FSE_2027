class Order:
    def __init__(self):
        self.menu = []
        self.selected_dishes = []
        self.sales = {}

    def addDish(self, dish):
        if dish is None or not all(k in dish for k in ['dish', 'price', 'count']):
            return False
        
        for menu_dish in self.menu:
            if dish['dish'] == menu_dish['dish']:
                dish_count = int(dish['count'])
                menu_dish_count = int(menu_dish['count'])
                
                if menu_dish_count < dish_count:
                    return False
                else:
                    menu_dish['count'] = menu_dish_count - dish_count
                    self.selected_dishes.append(dish)
                    return True
        
        return False

    def calculateTotal(self):
        total = 0.0
        for dish in self.selected_dishes:
            dish_name = dish['dish']
            price = dish['price']
            count = int(dish['count'])
            sale_factor = self.sales.get(dish_name, 1.0)
            total += price * count * sale_factor
        return total

    def checkout(self):
        if not self.selected_dishes:
            return False
        
        total = self.calculateTotal()
        self.selected_dishes.clear()
        return total