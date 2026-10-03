#include <unordered_map>
#include <string>
#include <optional>

class Warehouse {
private:
    // Nested class Product (equivalent to private static inner class in Java)
    class Product {
    private:
        std::string name;
        int quantity;

    public:
        Product(const std::string& name, int quantity)
            : name(name), quantity(quantity) {}

        void addQuantity(int qty) {
            quantity += qty;
        }

        int getQuantity() const {
            return quantity;
        }
    };

    // Nested class Order (equivalent to private static inner class in Java)
    class Order {
    private:
        int productId;
        int quantity;
        std::string status;

    public:
        Order(int productId, int quantity, const std::string& status)
            : productId(productId), quantity(quantity), status(status) {}

        const std::string& getStatus() const {
            return status;
        }

        void setStatus(const std::string& newStatus) {
            status = newStatus;
        }
    };

    std::unordered_map<int, Product> inventory;
    std::unordered_map<int, Order> orders;

public:
    Warehouse() = default;

    void addProduct(int productId, const std::string& name, int quantity) {
        auto it = inventory.find(productId);
        if (it != inventory.end()) {
            it->second.addQuantity(quantity);
        } else {
            inventory.emplace(productId, Product(name, quantity));
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
            orders.emplace(orderId, Order(productId, quantity, "Shipped"));
            return true;
        } else {
            return false;
        }
    }

    bool changeOrderStatus(int orderId, const std::string& status) {
        auto it = orders.find(orderId);
        if (it != orders.end()) {
            it->second.setStatus(status);
            return true;
        } else {
            return false;
        }
    }

    // Returns std::nullopt if order not found (mimics Java null)
    std::optional<std::string> trackOrder(int orderId) const {
        auto it = orders.find(orderId);
        if (it != orders.end()) {
            return it->second.getStatus();
        } else {
            return std::nullopt;
        }
    }
};