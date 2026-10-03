#ifndef VENDING_MACHINE_H
#define VENDING_MACHINE_H

#include <string>
#include <vector>
#include <utility>
#include <variant>
#include <sstream>
#include <iomanip>

namespace org::example {

class VendingMachine {
public:
    class Product {
    private:
        double price;
        int quantity;

    public:
        Product(double price, int quantity) : price(price), quantity(quantity) {}

        double getPrice() const { return price; }
        void setPrice(double price) { this->price = price; }
        int getQuantity() const { return quantity; }
        void setQuantity(int quantity) { this->quantity = quantity; }
    };

private:
    // LinkedHashMap preserves insertion order; vector does the same
    std::vector<std::pair<std::string, Product>> inventory;
    double balance;

    int findItem(const std::string& itemName) const {
        for (int i = 0; i < static_cast<int>(inventory.size()); i++) {
            if (inventory[i].first == itemName) {
                return i;
            }
        }
        return -1;
    }

public:
    VendingMachine() : balance(0) {}

    void addItem(const std::string& itemName, double price, int quantity) {
        if (!restockItem(itemName, quantity)) {
            inventory.emplace_back(itemName, Product(price, quantity));
        }
    }

    double insertCoin(double amount) {
        balance += amount;
        return balance;
    }

    // Java returns Object (Double or Boolean); use variant to match
    std::variant<double, bool> purchaseItem(const std::string& itemName) {
        int idx = findItem(itemName);
        if (idx >= 0) {
            Product& item = inventory[idx].second;
            if (item.getQuantity() > 0 && balance >= item.getPrice()) {
                balance -= item.getPrice();
                item.setQuantity(item.getQuantity() - 1);
                return balance;
            } else {
                return false;
            }
        } else {
            return false;
        }
    }

    bool restockItem(const std::string& itemName, int quantity) {
        int idx = findItem(itemName);
        if (idx >= 0) {
            Product& item = inventory[idx].second;
            item.setQuantity(item.getQuantity() + quantity);
            return true;
        } else {
            return false;
        }
    }

    // Java returns Object (String or Boolean); use variant to match
    std::variant<std::string, bool> displayItems() {
        if (inventory.empty()) {
            return false;
        } else {
            std::ostringstream items;
            for (const auto& entry : inventory) {
                const Product& item = entry.second;
                items << entry.first << " - $"
                      << std::fixed << std::setprecision(2) << item.getPrice()
                      << " [" << item.getQuantity() << "]\n";
            }
            std::string result = items.str();
            // Trim trailing whitespace to match Java's String.trim()
            while (!result.empty() && (result.back() == '\n' || result.back() == '\r'
                    || result.back() == ' ' || result.back() == '\t')) {
                result.pop_back();
            }
            return result;
        }
    }

    std::vector<std::pair<std::string, Product>>& getInventory() {
        return inventory;
    }

    void setInventory(const std::vector<std::pair<std::string, Product>>& inventory) {
        this->inventory = inventory;
    }

    double getBalance() const {
        return balance;
    }

    void setBalance(double balance) {
        this->balance = balance;
    }
};

} // namespace org::example

#endif // VENDING_MACHINE_H