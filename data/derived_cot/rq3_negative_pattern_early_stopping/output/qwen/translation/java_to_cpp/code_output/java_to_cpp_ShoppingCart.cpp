#include <unordered_map>
#include <string>

struct Item {
    double price;
    int quantity;

    Item(double price, int quantity) : price(price), quantity(quantity) {}

    bool operator==(const Item& other) const {
        return price == other.price && quantity == other.quantity;
    }
};

namespace std {
    template<> struct hash<Item> {
        size_t operator()(const Item& item) const {
            auto hasher = std::hash<double>{}(item.price);
            auto hasher2 = std::hash<int>{}(item.quantity);
            return hasher ^ (hasher2 << 1);
        }
    };
}

class ShoppingCart {
private:
    std::unordered_map<std::string, Item> items;

public:
    ShoppingCart() = default;

    void addItem(const std::string& item, double price, int quantity) {
        auto it = items.find(item);
        if (it != items.end()) {
            it->second.price = price;
            it->second.quantity += quantity;
        } else {
            items[item] = Item(price, quantity);
        }
    }

    void removeItem(const std::string& item, int quantity) {
        auto it = items.find(item);
        if (it != items.end()) {
            int newQuantity = it->second.quantity - quantity;
            if (newQuantity <= 0) {
                items.erase(it);
            } else {
                it->second.quantity = newQuantity;
            }
        }
    }

    std::unordered_map<std::string, Item> viewItems() const {
        return items;
    }

    double totalPrice() const {
        double total = 0.0;
        for (const auto& pair : items) {
            total += pair.second.price * pair.second.quantity;
        }
        return total;
    }
};