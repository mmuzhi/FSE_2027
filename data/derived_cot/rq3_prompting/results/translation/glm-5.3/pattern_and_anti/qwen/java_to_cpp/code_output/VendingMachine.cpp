#include <string>
#include <vector>
#include <utility>
#include <variant>
#include <sstream>
#include <iomanip>

class VendingMachine {
public:
    // Mirrors Java's static nested class Product
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

    // Preserves insertion order like LinkedHashMap<String, Product>
    using Inventory = std::vector<std::pair<std::string, Product>>;

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

    // Java returns Object: either Double (remaining balance) or Boolean false
    std::variant<double, bool> purchaseItem(const std::string& itemName) {
        Product* item = findProduct(itemName);
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
        Product* item = findProduct(itemName);
        if (item != nullptr) {
            item->setQuantity(item->getQuantity() + quantity);
            return true;
        } else {
            return false;
        }
    }

    // Java returns Object: either String (formatted items) or Boolean false
    std::variant<std::string, bool> displayItems() const {
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
            return trim(items.str());
        }
    }

    const Inventory& getInventory() const { return inventory; }
    Inventory& getInventory() { return inventory; }
    void setInventory(Inventory inventory) { this->inventory = std::move(inventory); }

    double getBalance() const { return balance; }
    void setBalance(double balance) { this->balance = balance; }

private:
    Inventory inventory;
    double balance;

    Product* findProduct(const std::string& itemName) {
        for (auto& entry : inventory) {
            if (entry.first == itemName) {
                return &entry.second;
            }
        }
        return nullptr;
    }

    // Mirrors Java's String.trim(): removes leading/trailing chars <= ' '
    static std::string trim(const std::string& s) {
        std::size_t begin = 0;
        std::size_t end = s.size();
        while (begin < end && static_cast<unsigned char>(s[begin]) <= ' ') {
            ++begin;
        }
        while (end > begin && static_cast<unsigned char>(s[end - 1]) <= ' ') {
            --end;
        }
        return s.substr(begin, end - begin);
    }
};