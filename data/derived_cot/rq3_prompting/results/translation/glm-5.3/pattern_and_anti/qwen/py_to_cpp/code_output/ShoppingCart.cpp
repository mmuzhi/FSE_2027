#include <map>
#include <string>

struct ItemInfo {
    double price;
    int quantity;
};

class ShoppingCart {
public:
    // Equivalent of Python's items = {} (item -> {"price": p, "quantity": q})
    ShoppingCart() = default;

    // Default quantity = 1; assignment overwrites any existing entry,
    // mirroring both branches of the Python add_item (identical bodies).
    void add_item(const std::string& item, double price, int quantity = 1) {
        items_[item] = ItemInfo{price, quantity};
    }

    // Subtract quantity only if the item exists; otherwise no-op.
    void remove_item(const std::string& item, int quantity = 1) {
        auto it = items_.find(item);
        if (it != items_.end()) {
            it->second.quantity -= quantity;
        }
    }

    // Returns the live internal map (reference), matching Python's
    // return of the dict object itself rather than a copy.
    std::map<std::string, ItemInfo>& view_items() {
        return items_;
    }

    // sum(quantity * price for each item) as a double.
    double total_price() const {
        double total = 0.0;
        for (const auto& entry : items_) {
            total += static_cast<double>(entry.second.quantity) * entry.second.price;
        }
        return total;
    }

private:
    std::map<std::string, ItemInfo> items_;
};