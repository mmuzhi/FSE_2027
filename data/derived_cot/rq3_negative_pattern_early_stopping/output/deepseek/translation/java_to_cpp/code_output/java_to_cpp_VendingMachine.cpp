#include <string>
#include <sstream>
#include <iomanip>
#include <vector>
#include <unordered_map>
#include <any>
#include <stdexcept>
#include <algorithm>

class VendingMachine {
public:
    struct Product {
        double price;
        int quantity;

        Product() : price(0.0), quantity(0) {}
        Product(double price, int quantity) : price(price), quantity(quantity) {}
    };

    VendingMachine() : balance_(0.0) {}

    void addItem(const std::string& itemName, double price, int quantity) {
        if (!restockItem(itemName, quantity)) {
            itemsOrder_.push_back({itemName, Product(price, quantity)});
            itemIndex_[itemName] = itemsOrder_.size() - 1;
        }
    }

    double insertCoin(double amount) {
        balance_ += amount;
        return balance_;
    }

    std::any purchaseItem(const std::string& itemName) {
        auto it = itemIndex_.find(itemName);
        if (it != itemIndex_.end()) {
            Product& item = itemsOrder_[it->second].second;
            if (item.quantity > 0 && balance_ >= item.price) {
                balance_ -= item.price;
                item.quantity -= 1;
                return std::any(balance_);
            } else {
                return std::any(false);
            }
        } else {
            return std::any(false);
        }
    }

    bool restockItem(const std::string& itemName, int quantity) {
        auto it = itemIndex_.find(itemName);
        if (it != itemIndex_.end()) {
            itemsOrder_[it->second].second.quantity += quantity;
            return true;
        }
        return false;
    }

    std::any displayItems() {
        if (itemsOrder_.empty()) {
            return std::any(false);
        } else {
            std::vector<std::string> lines;
            for (const auto& entry : itemsOrder_) {
                std::ostringstream oss;
                oss << entry.first << " - $"
                    << std::fixed << std::setprecision(2) << entry.second.price
                    << " [" << entry.second.quantity << "]";
                lines.push_back(oss.str());
            }
            std::ostringstream result;
            for (size_t i = 0; i < lines.size(); ++i) {
                if (i > 0) result << "\n";
                result << lines[i];
            }
            return std::any(result.str());
        }
    }

    // Getters and setters for inventory and balance
    std::unordered_map<std::string, Product> getInventory() const {
        std::unordered_map<std::string, Product> inv;
        for (const auto& entry : itemsOrder_) {
            inv[entry.first] = entry.second;
        }
        return inv;
    }

    void setInventory(const std::unordered_map<std::string, Product>& inventory) {
        itemsOrder_.clear();
        itemIndex_.clear();
        for (const auto& pair : inventory) {
            itemsOrder_.push_back(pair);
            itemIndex_[pair.first] = itemsOrder_.size() - 1;
        }
    }

    double getBalance() const { return balance_; }
    void setBalance(double balance) { balance_ = balance; }

private:
    std::vector<std::pair<std::string, Product>> itemsOrder_;
    std::unordered_map<std::string, size_t> itemIndex_;
    double balance_;
};