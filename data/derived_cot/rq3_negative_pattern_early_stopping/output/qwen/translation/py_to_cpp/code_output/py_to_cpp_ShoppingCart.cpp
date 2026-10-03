#include <iostream>
#include <unordered_map>
#include <string>
#include <vector>

struct ItemData {
    float price;
    int quantity;
};

class ShoppingCart {
private:
    std::unordered_map<std::string, ItemData> items;

public:
    ShoppingCart() : items() {}

    void add_item(const std::string& item, float price, int quantity = 1) {
        items[item] = {price, quantity};
    }

    void remove_item(const std::string& item, int quantity = 1) {
        if (items.find(item) != items.end()) {
            items[item].quantity -= quantity;
        }
    }

    std::unordered_map<std::string, ItemData> view_items() const {
        return items;
    }

    float total_price() const {
        float total = 0.0f;
        for (const auto& item : items) {
            total += static_cast<float>(item.second.quantity) * item.second.price;
        }
        return total;
    }
};

int main() {
    ShoppingCart cart;
    cart.add_item("apple", 1.0f, 5);
    cart.add_item("banana", 2.0f, 3);
    cart.remove_item("apple", 3);

    std::cout << "Items: ";
    for (const auto& item : cart.view_items()) {
        std::cout << item.first << ": " << item.second.quantity << " @ $" << item.second.price << " ";
    }
    std::cout << "\nTotal Price: $" << cart.total_price() << std::endl;

    return 0;
}