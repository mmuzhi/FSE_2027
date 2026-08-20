// Requires C++17 (std::variant).
// Translation of org.example.VendingMachine (Java).

#include <algorithm>
#include <cstddef>
#include <iomanip>
#include <sstream>
#include <string>
#include <utility>
#include <variant>
#include <vector>

namespace org::example {

class VendingMachine {
public:
    // Java's public static nested class Product.
    class Product {
    public:
        Product(double price, int quantity) : price_(price), quantity_(quantity) {}

        double getPrice() const { return price_; }

        void setPrice(double price) { price_ = price; }

        int getQuantity() const { return quantity_; }

        void setQuantity(int quantity) { quantity_ = quantity; }

    private:
        double price_;
        int quantity_;
    };

    // Java used LinkedHashMap<String, Product>: a keyed map that preserves
    // insertion order (relevant for displayItems' iteration order).
    // A vector of (key, Product) pairs reproduces those semantics for the
    // operations used here: containsKey / get / put (new key) / entrySet iteration.
    using Inventory = std::vector<std::pair<std::string, Product>>;

    VendingMachine() : balance_(0) {}

    void addItem(const std::string& itemName, double price, int quantity) {
        if (!restockItem(itemName, quantity)) {
            inventory_.emplace_back(itemName, Product(price, quantity));
        }
    }

    double insertCoin(double amount) {
        balance_ += amount;
        return balance_;
    }

    // Java returned Object: the new balance boxed as Double, or Boolean false.
    std::variant<double, bool> purchaseItem(const std::string& itemName) {
        auto it = findEntry(itemName);
        if (it != inventory_.end()) {
            Product& item = it->second;
            if (item.getQuantity() > 0 && balance_ >= item.getPrice()) {
                balance_ -= item.getPrice();
                item.setQuantity(item.getQuantity() - 1);
                return balance_;
            } else {
                return false;
            }
        } else {
            return false;
        }
    }

    bool restockItem(const std::string& itemName, int quantity) {
        auto it = findEntry(itemName);
        if (it != inventory_.end()) {
            it->second.setQuantity(it->second.getQuantity() + quantity);
            return true;
        }
        return false;
    }

    // Java returned Object: the formatted item list as String, or Boolean false.
    std::variant<std::string, bool> displayItems() const {
        if (inventory_.empty()) {
            return false;
        }
        std::ostringstream items;
        items << std::fixed << std::setprecision(2);
        for (const auto& entry : inventory_) {
            const Product& item = entry.second;
            items << entry.first << " - $" << item.getPrice() << " ["
                  << item.getQuantity() << "]\n";
        }
        return trim(items.str());
    }

    // Returns a live reference, mirroring Java's exposure of the internal map.
    Inventory& getInventory() { return inventory_; }
    const Inventory& getInventory() const { return inventory_; }

    void setInventory(Inventory inventory) { inventory_ = std::move(inventory); }

    double getBalance() const { return balance_; }

    void setBalance(double balance) { balance_ = balance; }

private:
    Inventory inventory_;
    double balance_;

    Inventory::iterator findEntry(const std::string& itemName) {
        return std::find_if(inventory_.begin(), inventory_.end(),
                            [&](const auto& entry) { return entry.first == itemName; });
    }

    // Equivalent of Java's String.trim(): strips leading/trailing chars <= U+0020.
    static std::string trim(const std::string& s) {
        std::size_t begin = 0;
        std::size_t end = s.size();
        while (begin < end && static_cast<unsigned char>(s[begin]) <= 0x20) {
            ++begin;
        }
        while (end > begin && static_cast<unsigned char>(s[end - 1]) <= 0x20) {
            --end;
        }
        return s.substr(begin, end - begin);
    }
};

}  // namespace org::example