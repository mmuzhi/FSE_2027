#include <any>
#include <map>
#include <string>
#include <vector>

class Order {
public:
    std::vector<std::map<std::string, std::any>> menu;
    std::vector<std::map<std::string, std::any>> selectedDishes;
    std::map<std::string, double> sales;

    Order() = default;

    // Pointer parameter preserves Java's null check on the incoming map.
    bool addDish(const std::map<std::string, std::any>* dish) {
        if (dish == nullptr
            || dish->find("dish") == dish->end()
            || dish->find("price") == dish->end()
            || dish->find("count") == dish->end()) {
            return false;
        }

        for (auto& menuDish : menu) {
            // std::any::operator== mirrors Object.equals (type + value).
            if (dish->at("dish") == menuDish.at("dish")) {
                int dishCount = std::any_cast<int>(dish->at("count"));
                int menuDishCount = std::any_cast<int>(menuDish.at("count"));

                if (menuDishCount < dishCount) {
                    return false;
                } else {
                    menuDish["count"] = menuDishCount - dishCount;
                    selectedDishes.push_back(*dish);
                    return true;
                }
            }
        }
        return false;
    }

    double calculateTotal() const {
        double total = 0;
        for (const auto& dish : selectedDishes) {
            const std::string& dishName = std::any_cast<const std::string&>(dish.at("dish"));
            double price = std::any_cast<double>(dish.at("price"));
            int count = std::any_cast<int>(dish.at("count"));
            double sale = 1.0; // 默认销售额为1 (getOrDefault)
            auto it = sales.find(dishName);
            if (it != sales.end()) {
                sale = it->second;
            }
            total += price * count * sale;
        }
        return total;
    }

    // std::any mirrors Java's polymorphic `Object` return (Boolean or Double).
    std::any checkout() {
        if (selectedDishes.empty()) {
            return false;
        }
        double total = calculateTotal();
        selectedDishes.clear();
        return total;
    }
};