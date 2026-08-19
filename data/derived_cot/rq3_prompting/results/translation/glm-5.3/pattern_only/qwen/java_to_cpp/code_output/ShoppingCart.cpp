#include <cstddef>
#include <cstdint>
#include <cstring>
#include <functional>
#include <string>
#include <unordered_map>

namespace org {
namespace example {

class ShoppingCart {
public:
    class Item {
    public:
        Item(double price, int quantity) : price_(price), quantity_(quantity) {}

        double getPrice() const { return price_; }
        void setPrice(double price) { price_ = price; }
        int getQuantity() const { return quantity_; }
        void setQuantity(int quantity) { quantity_ = quantity; }

        // Mirrors Java equals via Double.compare: bit-exact comparison
        // (so -0.0 != 0.0, and NaN compares equal to itself).
        bool operator==(const Item& other) const {
            return doubleBits(price_) == doubleBits(other.price_) &&
                   quantity_ == other.quantity_;
        }

        bool operator!=(const Item& other) const { return !(*this == other); }

        static std::uint64_t doubleBits(double d) {
            std::uint64_t bits = 0;
            std::memcpy(&bits, &d, sizeof(bits));
            return bits;
        }

    private:
        double price_;
        int quantity_;
    };

    ShoppingCart() = default;

    void addItem(const std::string& item, double price, int quantity) {
        auto it = items_.find(item);
        if (it != items_.end()) {
            it->second.setPrice(price);
            it->second.setQuantity(it->second.getQuantity() + quantity);
        } else {
            items_.emplace(item, Item(price, quantity));
        }
    }

    void removeItem(const std::string& item, int quantity) {
        auto it = items_.find(item);
        if (it != items_.end()) {
            int newQuantity = it->second.getQuantity() - quantity;
            if (newQuantity <= 0) {
                items_.erase(it);
            } else {
                it->second.setQuantity(newQuantity);
            }
        }
    }

    // Returns a copy of the map, like `new HashMap<>(items)`.
    std::unordered_map<std::string, Item> viewItems() const {
        return items_;
    }

    double totalPrice() const {
        double total = 0.0;
        for (const auto& entry : items_) {
            total += entry.second.getPrice() * entry.second.getQuantity();
        }
        return total;
    }

private:
    std::unordered_map<std::string, Item> items_;
};

}  // namespace example
}  // namespace org

// Mirrors Java hashCode: Objects.hash(price, quantity)
template <>
struct std::hash<org::example::ShoppingCart::Item> {
    std::size_t operator()(
        const org::example::ShoppingCart::Item& item) const {
        const std::uint64_t bits =
            org::example::ShoppingCart::Item::doubleBits(item.getPrice());
        const std::size_t priceHash =
            static_cast<std::size_t>(bits ^ (bits >> 32));  // Double.hashCode
        const std::size_t quantityHash =
            static_cast<std::size_t>(static_cast<unsigned>(item.getQuantity()));

        std::size_t result = 1;  // Arrays.hashCode seed
        result = 31 * result + priceHash;
        result = 31 * result + quantityHash;
        return result;
    }
};