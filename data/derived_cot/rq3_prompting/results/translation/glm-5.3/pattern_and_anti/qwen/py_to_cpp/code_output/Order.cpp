#include <map>
#include <optional>
#include <string>
#include <vector>

class Order {
public:
    // dish = {"dish": dish name, "price": price, "count": count}
    struct Dish {
        std::string dish;  // dish name
        double price;      // price
        int count;         // count
    };

    Order() = default;

    /*
      Check the menu and add into selected_dishes if the dish count is valid.
      If the dish has successfully been added, change the count in menu.
      Note: mirrors Python semantics — a dish not present in the menu is
      still appended to selected_dishes (loop simply never breaks/decrements).
      Returns true if successfully added, false otherwise.
    */
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

    /*
      Calculate the total price of dishes that have been ordered.
      Multiply the count, price and sales.
      Missing sale entry throws std::out_of_range (Python KeyError analog).
      Returns the final total price.
    */
    double calculate_total() const {
        double total = 0.0;
        for (const Dish& dish : selected_dishes) {
            total += dish.price * dish.count * sales.at(dish.dish);
        }
        return total;
    }

    /*
      Check out the dishes ordered. If selected_dishes is not empty,
      invoke calculate_total to check out.
      Returns std::nullopt (Python False) if selected_dishes is empty,
      otherwise the total (return value of calculate_total).
    */
    std::optional<double> checkout() {
        if (selected_dishes.empty()) {
            return std::nullopt;  // False
        }
        double total = calculate_total();
        selected_dishes.clear();
        return total;
    }

    std::vector<Dish> menu;                 // menu entries
    std::vector<Dish> selected_dishes;      // dishes selected by customer
    std::map<std::string, double> sales;    // {dish name: sales}
};