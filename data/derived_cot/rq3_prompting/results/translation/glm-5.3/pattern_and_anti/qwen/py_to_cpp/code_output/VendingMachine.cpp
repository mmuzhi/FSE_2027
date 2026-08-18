#include <string>
#include <vector>
#include <utility>
#include <optional>
#include <sstream>
#include <algorithm>

class VendingMachine {
public:
    struct Item {
        double price;
        int quantity;
    };

    VendingMachine() = default;

    // Adds a product to the vending machine's inventory.
    // If it already exists, restocks it instead.
    void add_item(const std::string& item_name, double price, int quantity) {
        if (!restock_item(item_name, quantity)) {
            inventory.emplace_back(item_name, Item{price, quantity});
        }
    }

    // Inserts coins; returns the balance after insertion.
    double insert_coin(double amount) {
        balance += amount;
        return balance;
    }

    // Purchases a product. Returns the balance on success,
    // or no value (Python False) on failure.
    std::optional<double> purchase_item(const std::string& item_name) {
        auto it = find(item_name);
        if (it != inventory.end()) {
            Item& item = it->second;
            if (item.quantity > 0 && balance >= item.price) {
                balance -= item.price;
                item.quantity -= 1;
                return balance;
            }
            return std::nullopt;
        }
        return std::nullopt;
    }

    // Replenishes inventory of an existing product.
    bool restock_item(const std::string& item_name, int quantity) {
        auto it = find(item_name);
        if (it != inventory.end()) {
            it->second.quantity += quantity;
            return true;
        }
        return false;
    }

    // Displays products. Returns no value (Python False) if empty,
    // otherwise a newline-joined string of items.
    std::optional<std::string> display_items() const {
        if (inventory.empty()) {
            return std::nullopt;
        }
        std::ostringstream items;
        for (size_t i = 0; i < inventory.size(); ++i) {
            if (i > 0) items << "\n";
            const auto& [name, info] = inventory[i];
            items << name << " - $" << info.price << " [" << info.quantity << "]";
        }
        return items.str();
    }

private:
    // Preserves Python dict insertion-order semantics.
    std::vector<std::pair<std::string, Item>> inventory;
    double balance = 0.0;

    std::vector<std::pair<std::string, Item>>::iterator find(const std::string& item_name) {
        return std::find_if(inventory.begin(), inventory.end(),
                            [&item_name](const auto& entry) {
                                return entry.first == item_name;
                            });
    }

    std::vector<std::pair<std::string, Item>>::const_iterator find(const std::string& item_name) const {
        return std::find_if(inventory.begin(), inventory.end(),
                            [&item_name](const auto& entry) {
                                return entry.first == item_name;
                            });
    }
};