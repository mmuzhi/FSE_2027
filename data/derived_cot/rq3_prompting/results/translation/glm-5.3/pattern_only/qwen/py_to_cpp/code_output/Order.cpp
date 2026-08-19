#include <string>
#include <vector>
#include <unordered_map>
#include <optional>

class Order {
public:
    struct Dish {
        std::string dish;   // dish name
        double price;
        int count;
    };

    // menu = [{"dish": dish name, "price": price, "count": count}, ...]
    std::vector<Dish> menu;
    // selected_dish = {"dish": dish name, "count": count, "price": price}
    std::vector<Dish> selected_dishes;
    // sales = {dish name: sales}
    std::unordered_map<std::string, double> sales;

    Order() = default;

    // Check the menu and add into selected_dishes if the dish count is valid.
    // Note: a dish not present in the menu is still appended (mirrors Python behavior).
    bool add_dish(const Dish& dish) {
        for (Dish& menu_dish : menu) {
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

    // Calculate the total price of dishes that have been ordered.
    // sales.at() throws std::out_of_range, mirroring Python's KeyError for missing dishes.
    double calculate_total() const {
        double total = 0;
        for (const Dish& dish : selected_dishes) {
            total += dish.price * dish.count * sales.at(dish.dish);
        }
        return total;
    }

    // Check out the dishes ordered; returns std::nullopt (Python False) when nothing is selected,
    // otherwise the total. selected_dishes is cleared only after a successful total computation,
    // matching Python's ordering.
    std::optional<double> checkout() {
        if (selected_dishes.empty()) {
            return std::nullopt;
        }
        double total = calculate_total();
        selected_dishes.clear();
        return total;
    }
};