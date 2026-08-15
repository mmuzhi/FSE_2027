#include <string>
#include <vector>
#include <utility>
#include <sstream>
#include <iomanip>
#include <variant>
#include <algorithm>
#include <cmath>

class VendingMachine {
public:
    class Product {
    public:
        Product(double price, int quantity) : price(price), quantity(quantity) {}

        double getPrice() const { return price; }
        void setPrice(double price) { this->price = price; }

        int getQuantity() const { return quantity; }
        void setQuantity(int quantity) { this->quantity = quantity; }

    private:
        double price;
        int quantity;
    };

    using Inventory = std::vector<std::pair<std::string, Product>>;

    VendingMachine() : balance(0.0) {}

    void addItem(const std::string& itemName, double price, int quantity) {
        if (!restockItem(itemName, quantity)) {
            inventory.emplace_back(itemName, Product(price, quantity));
        }
    }

    double insertCoin(double amount) {
        balance += amount;
        return balance;
    }

    std::variant<double, bool> purchaseItem(const std::string& itemName) {
        auto it = findItem(itemName);
        if (it != inventory.end()) {
            Product& item = it->second;
            if (item.getQuantity() > 0 && balance >= item.getPrice()) {
                balance -= item.getPrice();
                item.setQuantity(item.getQuantity() - 1);
                return balance;
            }
        }
        return false;
    }

    bool restockItem(const std::string& itemName, int quantity) {
        auto it = findItem(itemName);
        if (it != inventory.end()) {
            it->second.setQuantity(it->second.getQuantity() + quantity);
            return true;
        }
        return false;
    }

    std::variant<std::string, bool> displayItems() {
        if (inventory.empty()) {
            return false;
        }

        std::ostringstream oss;
        for (const auto& entry : inventory) {
            const Product& item = entry.second;
            oss << entry.first << " - $" << formatPrice(item.getPrice())
                << " [" << item.getQuantity() << "]\n";
        }

        return trim(oss.str());
    }

    Inventory& getInventory() { return inventory; }
    const Inventory& getInventory() const { return inventory; }

    void setInventory(const Inventory& newInventory) { inventory = newInventory; }

    double getBalance() const { return balance; }
    void setBalance(double balance) { this->balance = balance; }

private:
    Inventory inventory;
    double balance;

    Inventory::iterator findItem(const std::string& itemName) {
        return std::find_if(inventory.begin(), inventory.end(),
            [&itemName](const std::pair<std::string, Product>& entry) {
                return entry.first == itemName;
            });
    }

    Inventory::const_iterator findItem(const std::string& itemName) const {
        return std::find_if(inventory.begin(), inventory.end(),
            [&itemName](const std::pair<std::string, Product>& entry) {
                return entry.first == itemName;
            });
    }

    static std::string formatPrice(double price) {
        if (std::isnan(price)) return "NaN";
        if (std::isinf(price)) return price > 0 ? "Infinity" : "-Infinity";

        std::ostringstream oss;
        oss << std::fixed << std::setprecision(2) << price;
        return oss.str();
    }

    static std::string trim(const std::string& s) {
        size_t start = 0;
        while (start < s.size() && static_cast<unsigned char>(s[start]) <= ' ') {
            ++start;
        }
        size_t end = s.size();
        while (end > start && static_cast<unsigned char>(s[end - 1]) <= ' ') {
            --end;
        }
        return s.substr(start, end - start);
    }
};