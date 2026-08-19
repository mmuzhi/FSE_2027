#include <map>
#include <string>

class ShoppingCart {
public:
    struct ItemInfo {
        double price;
        int quantity;
    };

    ShoppingCart() = default;

    void add_item(const std::string& item, double price, int quantity = 1) {
        // Both branches of the original if/else perform the same overwrite.
        items[item] = ItemInfo{price, quantity};
    }

    void remove_item(const std::string& item, int quantity = 1) {
        auto it = items.find(item);
        if (it != items.end()) {
            it->second.quantity -= quantity;
        }
        // else: do nothing (matches the Python `pass`)
    }

    // Returns a reference to the live items, mirroring Python's
    // return of the underlying dict object.
    std::map<std::string, ItemInfo>& view_items() {
        return items;
    }

    const std::map<std::string, ItemInfo>& view_items() const {
        return items;
    }

    double total_price() const {
        double total = 0.0;
        for (const auto& entry : items) {
            total += entry.second.quantity * entry.second.price;
        }
        return total;
    }

private:
    std::map<std::string, ItemInfo> items;
};