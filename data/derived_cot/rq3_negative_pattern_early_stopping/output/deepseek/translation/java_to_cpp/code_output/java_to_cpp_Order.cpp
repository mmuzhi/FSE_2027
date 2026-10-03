#include <any>
#include <map>
#include <string>
#include <vector>

class Order {
public:
    Order() = default;

    bool addDish(const std::map<std::string, std::any>* dish) {
        // null dish -> false
        if (dish == nullptr) {
            return false;
        }
        // must contain all required keys
        if (dish->find("dish") == dish->end() ||
            dish->find("price") == dish->end() ||
            dish->find("count") == dish->end()) {
            return false;
        }

        // find matching dish in menu
        for (auto& menuDish : menu) {
            if (std::any_cast<std::string>(dish->at("dish")) ==
                std::any_cast<std::string>(menuDish.at("dish"))) {
                int dishCount = std::any_cast<int>(dish->at("count"));
                int menuCount = std::any_cast<int>(menuDish.at("count"));

                if (menuCount < dishCount) {
                    return false;
                } else {
                    menuDish["count"] = menuCount - dishCount;
                    // store a copy of the dish (same object semantics not preserved)
                    selectedDishes.push_back(*dish);
                    return true;
                }
            }
        }
        return false;
    }

    double calculateTotal() const {
        double total = 0.0;
        for (const auto& dish : selectedDishes) {
            std::string dishName = std::any_cast<std::string>(dish.at("dish"));
            double price = std::any_cast<double>(dish.at("price"));
            int count = std::any_cast<int>(dish.at("count"));

            auto it = sales.find(dishName);
            double sale = (it != sales.end()) ? it->second : 1.0;
            total += price * count * sale;
        }
        return total;
    }

    std::any checkout() {
        if (selectedDishes.empty()) {
            return false;
        }
        double total = calculateTotal();
        selectedDishes.clear();
        return total;
    }

private:
    std::vector<std::map<std::string, std::any>> menu;
    std::vector<std::map<std::string, std::any>> selectedDishes;
    std::map<std::string, double> sales;
};