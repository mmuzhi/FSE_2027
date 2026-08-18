#include <cmath>
#include <cstddef>
#include <cstdint>
#include <cstring>
#include <memory>
#include <string>
#include <unordered_map>

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
            return doubleEquals(price, other.price) && quantity == other.quantity;
        }

        bool operator!=(const Item& other) const { return !(*this == other); }

        // Mirrors Objects.hash(price, quantity): result = 31 * (31 * 1 + h(price)) + quantity,
        // with Java-style wrapping 32-bit arithmetic.
        std::int32_t hashCode() const {
            std::uint32_t h = 1u;
            h = 31u * h + static_cast<std::uint32_t>(javaDoubleHashCode(price));
            h = 31u * h + static_cast<std::uint32_t>(quantity);
            return static_cast<std::int32_t>(h);
        }

    private:
        double price;
        int quantity;

        // Mirrors Double.compare(a, b) == 0: NaN equals NaN, +0.0 != -0.0.
        static bool doubleEquals(double a, double b) {
            if (std::isnan(a) && std::isnan(b)) return true;
            if (a == 0.0 && b == 0.0) return std::signbit(a) == std::signbit(b);
            return a == b;
        }

        // Mirrors Double.hashCode: (bits ^ (bits >>> 32)) as int.
        static std::int32_t javaDoubleHashCode(double d) {
            std::uint64_t bits;
            std::memcpy(&bits, &d, sizeof(bits));
            std::uint32_t hi = static_cast<std::uint32_t>(bits >> 32);
            std::uint32_t lo = static_cast<std::uint32_t>(bits);
            return static_cast<std::int32_t>(hi ^ lo);
        }
    };

    ShoppingCart() = default;

    void addItem(const std::string& item, double price, int quantity) {
        auto it = items.find(item);
        if (it != items.end()) {
            std::shared_ptr<Item> existingItem = it->second; // copy before any potential mutation
            existingItem->setPrice(price);
            existingItem->setQuantity(existingItem->getQuantity() + quantity);
        } else {
            items.emplace(item, std::make_shared<Item>(price, quantity));
        }
    }

    void removeItem(const std::string& item, int quantity) {
        auto it = items.find(item);
        if (it != items.end()) {
            std::shared_ptr<Item> existingItem = it->second; // copy before erase (avoids dangling ref)
            int newQuantity = existingItem->getQuantity() - quantity;
            if (newQuantity <= 0) {
                items.erase(it);
            } else {
                existingItem->setQuantity(newQuantity);
            }
        }
    }

    // Shallow copy like Java: a new map whose values alias the same Item objects,
    // so mutating an Item via the returned map affects the cart's state.
    std::unordered_map<std::string, std::shared_ptr<Item>> viewItems() const {
        return items;
    }

    double totalPrice() const {
        double total = 0.0;
        for (const auto& entry : items) {
            total += entry.second->getPrice() * entry.second->getQuantity();
        }
        return total;
    }

private:
    std::unordered_map<std::string, std::shared_ptr<Item>> items;
};

namespace std {
template <>
struct hash<ShoppingCart::Item> {
    std::size_t operator()(const ShoppingCart::Item& item) const {
        return static_cast<std::size_t>(static_cast<std::uint32_t>(item.hashCode()));
    }
};
} // namespace std