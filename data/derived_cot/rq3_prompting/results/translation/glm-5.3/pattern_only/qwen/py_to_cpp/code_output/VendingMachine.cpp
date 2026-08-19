#include <charconv>
#include <optional>
#include <string>
#include <vector>

// This is a class to simulate a vending machine, including adding products,
// inserting coins, purchasing products, viewing balance, replenishing product
// inventory, and displaying product information.

class VendingMachine {
public:
    struct Item {
        double price;
        int quantity;
    };

    VendingMachine() = default;

    // Adds a product to the vending machine's inventory.
    // If the item already exists, it is restocked instead.
    void add_item(const std::string& item_name, double price, int quantity) {
        if (!restock_item(item_name, quantity)) {
            inventory.emplace_back(item_name, Item{price, quantity});
        }
    }

    // Inserts coins into the vending machine.
    // Returns the balance after the coins are inserted.
    double insert_coin(double amount) {
        balance += amount;
        return balance;
    }

    // Purchases a product. Returns the balance after purchase on success,
    // or no value (Python: False) if the product is missing, out of stock,
    // or the balance is insufficient.
    std::optional<double> purchase_item(const std::string& item_name) {
        Item* item = find(item_name);
        if (item != nullptr) {
            if (item->quantity > 0 && balance >= item->price) {
                balance -= item->price;
                item->quantity -= 1;
                return balance;
            } else {
                return std::nullopt;
            }
        } else {
            return std::nullopt;
        }
    }

    // Replenishes the inventory of a product already in the vending machine.
    // Returns true if the product exists, otherwise false.
    bool restock_item(const std::string& item_name, int quantity) {
        Item* item = find(item_name);
        if (item != nullptr) {
            item->quantity += quantity;
            return true;
        } else {
            return false;
        }
    }

    // Displays the products in the vending machine.
    // Returns no value (Python: False) if empty, otherwise a newline-joined
    // string of "name - $price [quantity]" in insertion order.
    std::optional<std::string> display_items() const {
        if (inventory.empty()) {
            return std::nullopt;
        } else {
            std::string items;
            for (std::size_t i = 0; i < inventory.size(); ++i) {
                if (i > 0) items += '\n';
                const auto& [item_name, item_info] = inventory[i];
                items += item_name;
                items += " - $";
                items += repr(item_info.price);
                items += " [";
                items += std::to_string(item_info.quantity);
                items += ']';
            }
            return items;
        }
    }

private:
    // Preserves Python dict insertion-order semantics for iteration.
    std::vector<std::pair<std::string, Item>> inventory;
    double balance = 0.0;

    Item* find(const std::string& name) {
        for (auto& entry : inventory) {
            if (entry.first == name) return &entry.second;
        }
        return nullptr;
    }

    // Mimics Python's f-string rendering of a float: shortest round-trip
    // representation, with a trailing ".0" for integral values.
    static std::string repr(double v) {
        char buf[64];
        auto res = std::to_chars(buf, buf + sizeof buf, v);
        std::string s(buf, res.ptr);
        if (!s.empty() &&
            s.find_first_not_of("0123456789+-") == std::string::npos) {
            s += ".0";
        }
        return s;
    }
};