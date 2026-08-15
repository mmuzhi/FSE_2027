#include <string>
#include <vector>
#include <map>
#include <variant>

struct Dish {
    std::string dish;
    double price;
    double count;
};

class Order {
public:
    Order() = default;

    bool add_dish(const Dish& dish) {
        for (auto& menu_dish : menu) {
            if (dish.dish == menu_dish.dish) {
                if (menu_dish.count < dish.count) {
                    return false;
                } else {
                    menu_dish.count -= dish.count;
                    break;
                }
            }
        }
        selected_dishes.push_back(dish);
        return true;
    }

    double calculate_total() {
        double total = 0.0;
        for (const auto& dish : selected_dishes) {
            total += dish.price * dish.count * sales.at(dish.dish);
        }
        return total;
    }

    std::variant<bool, double> checkout() {
        if (selected_dishes.empty()) {
            return false;
        }
        double total = calculate_total();
        selected_dishes.clear();
        return total;
    }

    std::vector<Dish> menu;
    std::vector<Dish> selected_dishes;
    std::map<std::string, double> sales;
};