#include <string>
#include <vector>
#include <variant>
#include <sstream>
#include <algorithm>

struct Item {
    double price;
    int quantity;
};

class VendingMachine {
private:
    std::vector<std::pair<std::string, Item>> inventory;
    double balance;

    auto find_item(const std::string& item_name) {
        return std::find_if(inventory.begin(), inventory.end(),
                            [&item_name](const auto& pair) { return pair.first == item_name; });
    }

public:
    VendingMachine() : balance(0.0) {}

    void add_item(std::string item_name, double price, int quantity) {
        if (!restock_item(item_name, quantity)) {
            inventory.emplace_back(std::move(item_name), Item{price, quantity});
        }
    }

    double insert_coin(double amount) {
        balance += amount;
        return balance;
    }

    std::variant<double, bool> purchase_item(const std::string& item_name) {
        auto it = find_item(item_name);
        if (it != inventory.end()) {
            if (it->second.quantity > 0 && balance >= it->second.price) {
                balance -= it->second.price;
                it->second.quantity -= 1;
                return balance;
            } else {
                return false;
            }
        } else {
            return false;
        }
    }

    bool restock_item(const std::string& item_name, int quantity) {
        auto it = find_item(item_name);
        if (it != inventory.end()) {
            it->second.quantity += quantity;
            return true;
        } else {
            return false;
        }
    }

    std::variant<std::string, bool> display_items() {
        if (inventory.empty()) {
            return false;
        } else {
            std::stringstream ss;
            for (size_t i = 0; i < inventory.size(); ++i) {
                if (i > 0) ss << "\n";
                ss << inventory[i].first << " - $" << inventory[i].second.price << " [" << inventory[i].second.quantity << "]";
            }
            return ss.str();
        }
    }
};