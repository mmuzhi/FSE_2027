#include <optional>
#include <string>
#include <unordered_map>
#include <utility>

namespace org {
namespace example {

class Warehouse {
public:
    Warehouse() = default;

    void addProduct(int productId, std::string name, int quantity) {
        auto it = inventory.find(productId);
        if (it != inventory.end()) {
            it->second.addQuantity(quantity);
        } else {
            inventory.insert_or_assign(productId, Product(std::move(name), quantity));
        }
    }

    void updateProductQuantity(int productId, int quantity) {
        auto it = inventory.find(productId);
        if (it != inventory.end()) {
            it->second.addQuantity(quantity);
        }
    }

    int getProductQuantity(int productId) const {
        auto it = inventory.find(productId);
        if (it != inventory.end()) {
            return it->second.getQuantity();
        } else {
            return -1;
        }
    }

    bool createOrder(int orderId, int productId, int quantity) {
        auto it = inventory.find(productId);
        if (it != inventory.end() && it->second.getQuantity() >= quantity) {
            it->second.addQuantity(-quantity);
            orders.insert_or_assign(orderId, Order(productId, quantity, "Shipped"));
            return true;
        } else {
            return false;
        }
    }

    bool changeOrderStatus(int orderId, std::string status) {
        auto it = orders.find(orderId);
        if (it != orders.end()) {
            it->second.setStatus(std::move(status));
            return true;
        } else {
            return false;
        }
    }

    std::optional<std::string> trackOrder(int orderId) const {
        auto it = orders.find(orderId);
        if (it != orders.end()) {
            return it->second.getStatus();
        } else {
            return std::nullopt;
        }
    }

private:
    class Product {
    public:
        Product(std::string name, int quantity)
            : name_(std::move(name)), quantity_(quantity) {}

        void addQuantity(int quantity) {
            quantity_ += quantity;
        }

        int getQuantity() const {
            return quantity_;
        }

    private:
        std::string name_;
        int quantity_;
    };

    class Order {
    public:
        Order(int productId, int quantity, std::string status)
            : productId_(productId), quantity_(quantity), status_(std::move(status)) {}

        const std::string& getStatus() const {
            return status_;
        }

        void setStatus(std::string status) {
            status_ = std::move(status);
        }

    private:
        int productId_;
        int quantity_;
        std::string status_;
    };

    std::unordered_map<int, Product> inventory;
    std::unordered_map<int, Order> orders;
};

} // namespace example
} // namespace org