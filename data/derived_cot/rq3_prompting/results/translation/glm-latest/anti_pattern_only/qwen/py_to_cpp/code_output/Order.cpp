#include <map>
#include <optional>
#include <string>
#include <vector>

// The class manages restaurant orders by allowing the addition of dishes,
// calculation of the total cost, and checkout.

// A dish entry. Used both for menu items
// ({"dish": dish name, "price": price, "count": count}) and for selected
// dishes ({"dish": dish name, "count": count, "price": price}).
struct Dish {
    std::string dish;  // dish name
    double price;      // price
    int count;         // count
};

class Order {
public:
    // menu stores the dishes of the restaurant inventory:
    //   menu = [{"dish": dish name, "price": price, "count": count}, ...]
    std::vector<Dish> menu;
    // selected_dishes stores the dishes selected by the customer:
    //   selected_dish = {"dish": dish name, "count": count, price: price}
    std::vector<Dish> selected_dishes;
    // sales stores the sales of each dish:
    //   sales = {dish name: sales}
    std::map<std::string, double> sales;

    // Initialize the order management system (all containers start empty).
    Order() = default;

    // Check the menu and add into selected_dishes if the dish count is valid.
    // If the dish has successfully been added, change the count in the menu.
    // dish: the information of the dish.
    // Returns true if successfully added, false otherwise.
    //
    //   Order order;
    //   order.menu.push_back({"dish1", 10.0, 5});
    //   order.add_dish({"dish1", 10.0, 3});   // -> true
    bool add_dish(const Dish& dish) {
        for (Dish& menu_dish : menu) {
            if (dish.dish == menu_dish.dish) {
                if (menu_dish.count < dish.count) {
                    return false;
                }
                menu_dish.count -= dish.count;
                break;
            }
        }
        selected_dishes.push_back(dish);
        return true;
    }

    // Calculate the total price of dishes that have been ordered.
    // Multiplies the count, price and sales.
    // Returns the final total price.
    // Throws std::out_of_range (the C++ analogue of Python's KeyError) if a
    // selected dish has no entry in sales.
    //
    //   Order order;
    //   order.menu.push_back({"dish1", 10.0, 5});
    //   order.sales["dish1"] = 0.8;
    //   order.add_dish({"dish1", 10.0, 4});   // -> true
    //   order.calculate_total();              // -> 32.0
    double calculate_total() const {
        double total = 0;
        for (const Dish& dish : selected_dishes) {
            // .at() throws for a missing key and performs no insertion,
            // exactly like self.sales[dish["dish"]] in Python.
            total += dish.price * dish.count * sales.at(dish.dish);
        }
        return total;
    }

    // Check out the dishes ordered. If selected_dishes is not empty, invoke
    // calculate_total to check out.
    // Returns std::nullopt (Python: False) if selected_dishes is empty,
    // otherwise the total (the return value of calculate_total).
    //
    //   Order order;
    //   order.menu.push_back({"dish1", 10.0, 5});
    //   order.sales["dish1"] = 0.8;
    //   order.add_dish({"dish1", 10.0, 4});   // -> true
    //   order.checkout();                     // -> 32.0
    std::optional<double> checkout() {
        if (selected_dishes.empty()) {
            return std::nullopt;  // Python: False
        }
        double total = calculate_total();
        selected_dishes.clear();  // Python: self.selected_dishes = []
        return total;
    }
};