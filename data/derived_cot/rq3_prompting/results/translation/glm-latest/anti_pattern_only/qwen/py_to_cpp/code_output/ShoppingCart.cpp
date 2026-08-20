#include <string>
#include <utility>
#include <vector>

// The class manages items, their prices, quantities, and allows to add,
// remove, view items, and calculate the total price.
class ShoppingCart {
public:
    // Analog of the Python per-item dict: {'price': float, 'quantity': int}
    struct ItemInfo {
        double price;
        int quantity;
    };

    // Analog of the Python 'items' dict: a mapping from item name to
    // {price, quantity} that preserves insertion order (like a Python dict).
    using Items = std::vector<std::pair<std::string, ItemInfo>>;

    ShoppingCart() = default;

    // Add item information to the shopping list items, including price and
    // quantity. The default quantity is 1. An existing entry is overwritten
    // (same as the Python original, whose if/else branches are identical),
    // keeping its original position in the container.
    void add_item(const std::string& item, double price, int quantity = 1) {
        for (auto& entry : items_) {
            if (entry.first == item) {
                entry.second.price = price;
                entry.second.quantity = quantity;
                return;
            }
        }
        items_.emplace_back(item, ItemInfo{price, quantity});
    }

    // Subtract the specified quantity of item from the shopping list items.
    // If the item is not present, do nothing. The quantity may become zero or
    // negative; the entry is never removed (matches Python behavior).
    void remove_item(const std::string& item, int quantity = 1) {
        for (auto& entry : items_) {
            if (entry.first == item) {
                entry.second.quantity -= quantity;
                return;
            }
        }
        // item not found: pass (no-op)
    }

    // Return the current shopping list items (a reference to the live
    // container, mirroring `return self.items` in Python).
    Items& view_items() { return items_; }
    const Items& view_items() const { return items_; }

    // Calculate the total price of all items in the shopping list:
    // the quantity of each item multiplied by the price, summed in
    // insertion order (Python dict iteration order).
    double total_price() const {
        double total = 0.0;
        for (const auto& entry : items_) {
            total += static_cast<double>(entry.second.quantity) * entry.second.price;
        }
        return total;
    }

private:
    Items items_;
};