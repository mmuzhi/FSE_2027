#include <unordered_map>
#include <string>
#include <cstdint>
#include <cstring>
#include <cmath>
#include <functional>

class ShoppingCart {
private:
    static int64_t doubleToLongBits(double d) {
        if (std::isnan(d)) {
            return 0x7ff8000000000000LL;
        }
        int64_t bits;
        std::memcpy(&bits, &d, sizeof(double));
        return bits;
    }

    static bool DoubleEquals(double a, double b) {
        return doubleToLongBits(a) == doubleToLongBits(b);
    }

public:
    class Item {
    private:
        double price;
        int quantity;

    public:
        Item(double price, int quantity) : price(price), quantity(quantity) {}

        double getPrice() const {
            return price;
        }

        void setPrice(double price) {
            this->price = price;
        }

        int getQuantity() const {
            return quantity;
        }

        void setQuantity(int quantity) {
            this->quantity = quantity;
        }

        bool operator==(const Item& other) const {
            return DoubleEquals(price, other.price) && quantity == other.quantity;
        }
    };

private:
    std::unordered_map<std::string, Item> items;

public:
    ShoppingCart() = default;

    void addItem(const std::string& item, double price, int quantity) {
        auto it = items.find(item);
        if (it != items.end()) {
            it->second.setPrice(price);
            it->second.setQuantity(it->second.getQuantity() + quantity);
        } else {
            items.emplace(item, Item(price, quantity));
        }
    }

    void removeItem(const std::string& item, int quantity) {
        auto it = items.find(item);
        if (it != items.end()) {
            int newQuantity = it->second.getQuantity() - quantity;
            if (newQuantity <= 0) {
                items.erase(it);
            } else {
                it->second.setQuantity(newQuantity);
            }
        }
    }

    std::unordered_map<std::string, Item> viewItems() const {
        return items;
    }

    double totalPrice() const {
        double total = 0.0;
        for (const auto& pair : items) {
            total += pair.second.getPrice() * pair.second.getQuantity();
        }
        return total;
    }
};

namespace std {
    template <>
    struct hash<ShoppingCart::Item> {
        size_t operator()(const ShoppingCart::Item& item) const {
            double d = item.getPrice();
            int64_t bits;
            if (std::isnan(d)) {
                bits = 0x7ff8000000000000LL;
            } else {
                std::memcpy(&bits, &d, sizeof(double));
            }
            unsigned int u_double_hash = static_cast<unsigned int>(bits ^ (bits >> 32));
            unsigned int u_quantity = static_cast<unsigned int>(item.getQuantity());
            
            unsigned int result = 1;
            result = 31 * result + u_double_hash;
            result = 31 * result + u_quantity;
            return static_cast<size_t>(static_cast<int>(result));
        }
    };
}