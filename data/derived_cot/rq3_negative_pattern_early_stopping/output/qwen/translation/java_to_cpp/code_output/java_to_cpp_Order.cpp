#include <vector>
#include <map>
#include <string>
#include <variant>

struct Dish {
    std::string name;
    double price;
    int count;
};

class Order {
private:
    std::vector<Dish> menu;
    std::vector<Dish> selectedDishes;
    std::map<std::string, double> sales;

public:
    Order() : menu(), selectedDishes(), sales() {}

    bool addDish(const Dish& dish) {
        // Validate dish data
        if (!dish.name.empty() && dish.price >= 0 && dish.count > 0) {
            for (Dish& menuDish : menu) {
                if (dish.name == menuDish.name) {
                    if (menuDish.count < dish.count) {
                        return false;
                    } else {
                        menuDish.count -= dish.count;
                        selectedDishes.push_back(dish);
                        return true;
                    }
                }
            }
            return false;
        }
        return false;
    }

    double calculateTotal() const {
        double total = 0;
        for (const Dish& dish : selectedDishes) {
            double sale = sales.find(dish.name) != sales.end() 
                          ? sales.at(dish.name) 
                          : 1.0;
            total += dish.price * dish.count * sale;
        }
        return total;
    }

    std::variant<bool, double> checkout() {
        if (selectedDishes.empty()) {
            return false;
        }
        double total = calculateTotal();
        selectedDishes.clear();
        return total;
    }
};