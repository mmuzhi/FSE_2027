#include <unordered_map>
#include <string>
#include <cmath>
#include <functional>
#include <stdexcept> // for std::hash specialization if needed

class ShoppingCart {
public:
    // Nested class Item (equivalent to Java static inner class)
    class Item {
    private:
        double price;
        int quantity;

    public:
        Item(double price, int quantity) : price(price), quantity(quantity) {}

        double getPrice() const { return price; }
        void setPrice(double p) { price = p; }

        int getQuantity() const { return quantity; }
        void setQuantity(int q) { quantity = q; }

        // Equality operator matching Java's equals() behavior
        bool operator==(const Item& other) const {
            // Handle NaN: two NaN values are considered equal
            if (std::isnan(price) && std::isnan(other.price)) {
                return quantity == other.quantity;
            }
            // If one is NaN and the other is not, they are not equal
            if (std::isnan(price) || std::isnan(other.price)) {
                return false;
            }
            // Usual comparison
            return price == other.price && quantity == other.quantity;
        }

        // Inequality operator (optional, but good practice)
        bool operator!=(const Item& other) const {
            return !(*this == other);
        }
    };

    // Constructor
    ShoppingCart() = default;

    // Add item (if exists, update price and quantity; otherwise insert)
    void addItem(const std::string& item, double price, int quantity) {
        auto it = items.find(item);
        if (it != items.end()) {
            it->second.setPrice(price);
            it->second.setQuantity(it->second.getQuantity() + quantity);
        } else {
            items.emplace(item, Item(price, quantity));
        }
    }

    // Remove quantity of an item; if result <= 0, remove the item entirely
    void removeItem(const std::string& item, int quantity) {
        auto it = items.find(item);
        if (it != items.end()) {
            int newQuantity = it->second.getQuantity() - quantity;
            if (newQuantity <= 0) {
                items.erase(it);
            } else {
                it->second.setQuantity(newQuantity);
            }
        }
    }

    // Return a copy of the current items map
    std::unordered_map<std::string, Item> viewItems() const {
        return items; // copy
    }

    // Compute total price of all items (price * quantity)
    double totalPrice() const {
        double total = 0.0;
        for (const auto& pair : items) {
            const Item& item = pair.second;
            total += item.getPrice() * item.getQuantity();
        }
        return total;
    }

private:
    std::unordered_map<std::string, Item> items;
};

// Specialize std::hash for ShoppingCart::Item (not strictly needed but matches Java's hashCode)
namespace std {
    template <>
    struct hash<ShoppingCart::Item> {
        size_t operator()(const ShoppingCart::Item& item) const {
            // Combine hash of price and quantity using std::hash.
            // For NaN consistency, we treat all NaN as having the same hash.
            double price = item.getPrice();
            size_t h1 = std::isnan(price) ? std::hash<double>()(0.0) : std::hash<double>()(price);
            size_t h2 = std::hash<int>()(item.getQuantity());
            // Boost-like combine (commonly used)
            return h1 ^ (h2 + 0x9e3779b9 + (h1 << 6) + (h1 >> 2));
        }
    };
}