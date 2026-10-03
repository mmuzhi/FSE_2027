#include <string>
#include <unordered_map>
#include <sstream>
#include <iomanip>
#include <optional>

class VendingMachine {
private:
    struct Item {
        double price;
        int quantity;
    };
    std::unordered_map<std::string, Item> inventory;
    double balance;

public:
    VendingMachine() : balance(0.0) {}

    void add_item(const std::string& item_name, double price, int quantity) {
        auto it = inventory.find(item_name);
        if (it != inventory.end()) {
            it->second.quantity += quantity;
        } else {
            inventory[item_name] = Item{price, quantity};
        }
    }

    double insert_coin(double amount) {
        balance += amount;
        return balance;
    }

    std::optional<double> purchase_item(const std::string& item_name) {
        auto it = inventory.find(item_name);
        if (it == inventory.end()) {
            return std::nullopt;
        }
        Item& item = it->second;
        if (item.quantity <= 0 || balance < item.price) {
            return std::nullopt;
        }
        balance -= item.price;
        item.quantity -= 1;
        return balance;
    }

    bool restock_item(const std::string& item_name, int quantity) {
        auto it = inventory.find(item_name);
        if (it != inventory.end()) {
            it->second.quantity += quantity;
            return true;
        }
        return false;
    }

    // Returns false if empty, otherwise a string representation.
    // The C++ version returns an optional string to match Python's behavior
    // (False vs string). We use std::optional<std::string>.
    std::optional<std::string> display_items() const {
        if (inventory.empty()) {
            return std::nullopt;
        }
        std::ostringstream oss;
        bool first = true;
        for (const auto& [name, item] : inventory) {
            if (!first) {
                oss << "\n";
            }
            first = false;
            oss << name << " - $" << std::fixed << std::setprecision(2) << item.price << " [" << item.quantity << "]";
        }
        return oss.str();
    }
};