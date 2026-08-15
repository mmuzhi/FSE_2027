#include <string>
#include <unordered_map>
#include <memory>
#include <cstring>
#include <cmath>
#include <cstdint>
#include <functional>

class ShoppingCart {
public:
    class Item {
    public:
        Item(double price, int quantity) : price(price), quantity(quantity) {}

        double getPrice() const { return price; }
        void setPrice(double price) { this->price = price; }
        int getQuantity() const { return quantity; }
        void setQuantity(int quantity) { this->quantity = quantity; }

        bool operator==(const Item& other) const {
            return doubleCompare(price, other.price) == 0 && quantity == other.quantity;
        }

        bool operator!=(const Item& other) const {
            return !(*this == other);
        }

        int hashCode() const {
            uint32_t result = 1;
            result = 31 * result + static_cast<uint32_t>(doubleHashCode(price));
            result = 31 * result + static_cast<uint32_t>(quantity);
            return static_cast<int>(result);
        }

    private:
        double price;
        int quantity;

        static int64_t doubleToLongBits(double value) {
            if (std::isnan(value)) {
                return 0x7ff8000000000000LL;
            }
            int64_t bits;
            std::memcpy(&bits, &value, sizeof(double));
            return bits;
        }

        static int doubleHashCode(double value) {
            uint64_t bits = static_cast<uint64_t>(doubleToLongBits(value));
            return static_cast<int>(bits ^ (bits >> 32));
        }

        static int doubleCompare(double d1, double d2) {
            if (d1 < d2) return -1;
            if (d1 > d2) return 1;
            int64_t bits1 = doubleToLongBits(d1);
            int64_t bits2 = doubleToLongBits(d2);
            if (bits1 == bits2) return 0;
            return bits1 < bits2 ? -1 : 1;
        }
    };

    ShoppingCart() {}

    void addItem(const std::string& item, double price, int quantity) {
        auto it = items.find(item);
        if (it != items.end()) {
            it->second->setPrice(price);
            it->second->setQuantity(it->second->getQuantity() + quantity);
        } else {
            items.emplace(item, std::make_shared<Item>(price, quantity));
        }
    }

    void removeItem(const std::string& item, int quantity) {
        auto it = items.find(item);
        if (it != items.end()) {
            int newQuantity = it->second->getQuantity() - quantity;
            if (newQuantity <= 0) {
                items.erase(it);
            } else {
                it->second->setQuantity(newQuantity);
            }
        }
    }

    std::unordered_map<std::string, std::shared_ptr<Item>> viewItems() const {
        return items;
    }

    double totalPrice() const {
        double total = 0.0;
        for (const auto& pair : items) {
            total += pair.second->getPrice() * pair.second->getQuantity();
        }
        return total;
    }

private:
    std::unordered_map<std::string, std::shared_ptr<Item>> items;
};

namespace std {
    template<>
    struct hash<ShoppingCart::Item> {
        size_t operator()(const ShoppingCart::Item& item) const {
            return static_cast<size_t>(static_cast<uint32_t>(item.hashCode()));
        }
    };
}