#include <string>
#include <vector>
#include <map>
#include <stdexcept>

class Order {
public:
    struct DishInfo {
        std::string dish;
        double price;
        int count;
    };

    std::vector<DishInfo> menu;
    std::vector<DishInfo> selected_dishes;
    std::map<std::string, double> sales;

    Order() {}

    bool add_dish(const DishInfo& dish) {
        bool found = false;
        for (auto& menu_dish : menu) {
            if (dish.dish == menu_dish.dish) {
                if (menu_dish.count < dish.count) {
                    return false;
                }
                menu_dish.count -= dish.count;
                found = true;
                break;
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

    double checkout() {
        if (selected_dishes.empty()) {
            return 0.0;  // In the Python code this returns False, which converts to 0.0 in numeric contexts.
                         // We return 0.0 to preserve falsy value.
        }
        double total = calculate_total();
        selected_dishes.clear();
        return total;
    }
};