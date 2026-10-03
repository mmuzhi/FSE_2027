#include <vector>
#include <unordered_map>
#include <optional>
#include <string>

struct Dish {
    std::string name;
    float price;
    int count;
};

class Order {
public:
    bool add_dish(const Dish& dish) {
        for (auto& menu_dish : menu) {
            if (menu_dish.name == dish.name) {
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

    float calculate_total() const {
        float total = 0.0f;
        for (const auto& dish : selected_dishes) {
            total += dish.price * dish.count * sales.at(dish.name);
        }
        return total;
    }

    std::optional<float> checkout() {
        if (selected_dishes.empty()) {
            return std::nullopt;
        }
        float total = calculate_total();
        selected_dishes.clear();
        return total;
    }

private:
    std::vector<Dish> menu;
    std::vector<Dish> selected_dishes;
    std::unordered_map<std::string, float> sales;
};