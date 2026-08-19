#include <any>
#include <string>
#include <unordered_map>
#include <map>
#include <vector>

namespace org::example {

class Order {
public:
    std::vector<std::map<std::string, std::any>> menu;
    std::vector<std::map<std::string, std::any>> selectedDishes;
    std::unordered_map<std::string, double> sales;

    Order() = default;

    bool addDish(std::map<std::string, std::any>& dish) {
        if (dish.find("dish") == dish.end() ||
            dish.find("price") == dish.end() ||
            dish.find("count") == dish.end()) {
            return false;
        }

        for (auto& menuDish : menu) {
            if (std::any_cast<const std::string&>(dish.at("dish")) ==
                std::any_cast<const std::string&>(menuDish.at("dish"))) {
                int dishCount = std::any_cast<int>(dish.at("count"));
                int menuDishCount = std::any_cast<int>(menuDish.at("count"));

                if (menuDishCount < dishCount) {
                    return false;
                } else {
                    menuDish["count"] = menuDishCount - dishCount;
                    selectedDishes.push_back(dish);
                    return true;
                }
            }
        }
        return false;
    }

    double calculateTotal() {
        double total = 0;
        for (auto& dish : selectedDishes) {
            const std::string& dishName = std::any_cast<const std::string&>(dish.at("dish"));
            double price = std::any_cast<double>(dish.at("price"));
            int count = std::any_cast<int>(dish.at("count"));
            auto it = sales.find(dishName);
            double sale = (it != sales.end()) ? it->second : 1.0; // 默认销售额为1
            total += price * count * sale;
        }
        return total;
    }

    std::any checkout() {
        if (selectedDishes.empty()) {
            return std::any(false);
        }
        double total = calculateTotal();
        selectedDishes.clear();
        return std::any(total);
    }
};

} // namespace org::example