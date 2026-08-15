#include <unordered_map>
#include <vector>
#include <variant>
#include <string>
#include <memory>
#include <stdexcept>

class NullPointerException : public std::runtime_error {
public:
    NullPointerException() : std::runtime_error("NullPointerException") {}
};

using Value = std::variant<std::monostate, int, double, std::string>;
using Dish = std::unordered_map<std::string, Value>;
using DishPtr = std::shared_ptr<Dish>;

struct Order {
    std::vector<DishPtr> menu;
    std::vector<DishPtr> selectedDishes;
    std::unordered_map<std::string, double> sales;

    Order() = default;

    bool addDish(const DishPtr& dish) {
        if (!dish) return false;
        if (dish->find("dish") == dish->end() ||
            dish->find("price") == dish->end() ||
            dish->find("count") == dish->end()) {
            return false;
        }

        const Value& dishName = findValue(*dish, "dish");
        if (std::holds_alternative<std::monostate>(dishName)) {
            throw NullPointerException();
        }

        for (const auto& menuDish : menu) {
            if (!menuDish) {
                throw NullPointerException();
            }
            const Value& menuDishName = findValue(*menuDish, "dish");
            if (dishName == menuDishName) {
                int dishCount = getValue<int>(*dish, "count");
                int menuDishCount = getValue<int>(*menuDish, "count");
                if (menuDishCount < dishCount) {
                    return false;
                } else {
                    (*menuDish)["count"] = menuDishCount - dishCount;
                    selectedDishes.push_back(dish);
                    return true;
                }
            }
        }
        return false;
    }

    double calculateTotal() const {
        double total = 0;
        for (const auto& dish : selectedDishes) {
            if (!dish) {
                throw NullPointerException();
            }
            std::string dishName = getValue<std::string>(*dish, "dish");
            double price = getValue<double>(*dish, "price");
            int count = getValue<int>(*dish, "count");
            double sale = 1.0;
            auto it = sales.find(dishName);
            if (it != sales.end()) {
                sale = it->second;
            }
            total += price * count * sale;
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

private:
    template<typename T>
    static T getValue(const Dish& dish, const std::string& key) {
        auto it = dish.find(key);
        if (it == dish.end()) {
            throw NullPointerException();
        }
        const Value& v = it->second;
        if (std::holds_alternative<std::monostate>(v)) {
            throw NullPointerException();
        }
        return std::get<T>(v);
    }

    static const Value& findValue(const Dish& dish, const std::string& key) {
        static const Value nullValue = std::monostate{};
        auto it = dish.find(key);
        if (it == dish.end()) {
            return nullValue;
        }
        return it->second;
    }
};