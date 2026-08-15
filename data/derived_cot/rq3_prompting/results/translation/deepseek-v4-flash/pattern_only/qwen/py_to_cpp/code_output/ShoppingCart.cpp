#include <map>
#include <string>

class ShoppingCart {
public:
    struct Item {
        double price;
        int quantity;
    };

    void add_item(const std::string& item, double price, int quantity = 1) {
        items_[item] = Item{price, quantity};
    }

    void remove_item(const std::string& item, int quantity = 1) {
        auto it = items_.find(item);
        if (it != items_.end()) {
            it->second.quantity -= quantity;
        }
    }

    std::map<std::string, Item>& view_items() {
        return items_;
    }

    const std::map<std::string, Item>& view_items() const {
        return items_;
    }

    double total_price() const {
        double total = 0.0;
        for (const auto& entry : items_) {
            total += entry.second.quantity * entry.second.price;
        }
        return total;
    }

private:
    std::map<std::string, Item> items_;
};