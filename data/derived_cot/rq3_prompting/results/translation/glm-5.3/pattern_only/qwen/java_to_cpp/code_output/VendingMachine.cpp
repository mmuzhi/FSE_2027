#include <cstddef>
#include <cstdio>
#include <string>
#include <utility>
#include <variant>
#include <vector>

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

    // Java returns Object: Double (remaining balance) on success, Boolean false otherwise.
    std::variant<double, bool> purchaseItem(const std::string& itemName) {
        Product* item = findItem(itemName);
        if (item != nullptr) {
            if (item->getQuantity() > 0 && balance >= item->getPrice()) {
                balance -= item->getPrice();
                item->setQuantity(item->getQuantity() - 1);
                return balance;
            } else {
                return false;
            }
        } else {
            return false;
        }
    }

    bool restockItem(const std::string& itemName, int quantity) {
        Product* item = findItem(itemName);
        if (item != nullptr) {
            item->setQuantity(item->getQuantity() + quantity);
            return true;
        } else {
            return false;
        }
    }

    // Java returns Object: String of items, or Boolean false when empty.
    std::variant<std::string, bool> displayItems() const {
        if (inventory.empty()) {
            return false;
        } else {
            std::string items;
            for (const auto& entry : inventory) {
                const Product& item = entry.second;
                char buffer[256];
                std::snprintf(buffer, sizeof(buffer), "%s - $%.2f [%d]\n",
                              entry.first.c_str(), item.getPrice(), item.getQuantity());
                items += buffer;
            }
            return trim(items);
        }
    }

    // Preserves insertion order like LinkedHashMap (affects displayItems order).
    std::vector<std::pair<std::string, Product>>& getInventory() { return inventory; }
    void setInventory(std::vector<std::pair<std::string, Product>> inventory) {
        this->inventory = std::move(inventory);
    }

    double getBalance() const { return balance; }
    void setBalance(double balance) { this->balance = balance; }

private:
    std::vector<std::pair<std::string, Product>> inventory;
    double balance;

    Product* findItem(const std::string& itemName) {
        for (auto& entry : inventory) {
            if (entry.first == itemName) {
                return &entry.second;
            }
        }
        return nullptr;
    }

    const Product* findItem(const std::string& itemName) const {
        for (const auto& entry : inventory) {
            if (entry.first == itemName) {
                return &entry.second;
            }
        }
        return nullptr;
    }

    // Equivalent of Java's String.trim(): strips leading/trailing chars <= ' '.
    static std::string trim(const std::string& s) {
        std::size_t begin = 0;
        std::size_t end = s.size();
        while (begin < end && s[begin] <= ' ') ++begin;
        while (end > begin && s[end - 1] <= ' ') --end;
        return s.substr(begin, end - begin);
    }
};