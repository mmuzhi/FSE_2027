#include <map>
#include <string>
#include <stdexcept>

class ShoppingCart {
public:
    struct Item {
        double price;
        int quantity;
    };

private:
    std::map<std::string, Item> items;

public:
    ShoppingCart() {}

    void add_item(const std::string& item, double price, int quantity = 1) {
        items[item] = {price, quantity};
    }

    void remove_item(const std::string& item, int quantity = 1) {
        auto it = items.find(item);
        if (it != items.end()) {
            it->second.quantity -= quantity;
        }
    }

    std::map<std::string, Item>& view_items() {
        return items;
    }

    double total_price() const {
        double total = 0.0;
        for (const auto& pair : items) {
            total += pair.second.quantity * pair.second.price;
        }
        return total;
    }
};