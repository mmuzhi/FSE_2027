#include <iostream>
#include <map>
#include <string>
#include <vector>
#include <iomanip>

class VendingMachine {
private:
    std::map<std::string, std::map<std::string, int>> inventory; // Format: {itemName: { "price": int, "quantity": int }}
    double balance;

public:
    VendingMachine() : balance(0.0) {}

    void add_item(std::string item_name, double price, int quantity) {
        // Check if the item already exists
        if (inventory.find(item_name) != inventory.end()) {
            // If it exists, we don't add again, but we might want to update the quantity? 
            // But the problem says "adds a product", so we should only add if it doesn't exist.
            // However, the Python code only adds if it doesn't exist. So we'll do the same.
            return;
        }
        inventory[item_name]["price"] = static_cast<int>(price * 100); // Store as cents to avoid floating point issues
        inventory[item_name]["quantity"] = quantity;
    }

    double insert_coin(double amount) {
        balance += amount;
        return balance;
    }

    bool purchase_item(std::string item_name) {
        // Check if the item exists and has quantity
        auto it = inventory.find(item_name);
        if (it == inventory.end()) {
            return false;
        }

        int price_cents = it->second["price"];
        int quantity = it->second["quantity"];

        if (quantity <= 0) {
            return false;
        }

        if (balance < price_cents / 100.0) { // Convert back to dollars for comparison
            return false;
        }

        // Deduct the price and reduce quantity
        balance -= price_cents / 100.0;
        it->second["quantity"] = quantity - 1;

        return balance;
    }

    bool restock_item(std::string item_name, int quantity) {
        auto it = inventory.find(item_name);
        if (it == inventory.end()) {
            return false;
        }

        it->second["quantity"] += quantity;
        return true;
    }

    std::string display_items() {
        if (inventory.empty()) {
            return "False";
        }

        std::string result;
        for (auto& item : inventory) {
            double price = item.second["price"] / 100.0;
            result += item.first + " - $" + std::to_string(price) + " [" + std::to_string(item.second["quantity"]) + "]\n";
        }

        return result;
    }
};