#include <unordered_map>
#include <string>
#include <optional>
#include <utility>

class Warehouse {
private:
    class Product {
    public:
        std::string name;
        int quantity;

        Product(const std::string& name, int quantity) : name(name), quantity(quantity) {}

        void addQuantity(int q) {
            quantity += q;
        }

        int getQuantity() const {
            return quantity;
        }
    };

    class Order {
    public:
        int productId;
        int quantity;
        std::string status;

        Order(int productId, int quantity, const std::string& status)
            : productId(productId), quantity(quantity), status(status) {}

        std::string getStatus() const {
            return status;
        }

        void setStatus(const std::string& s) {
            status = s;
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
        }
        return -1;
    }

    bool createOrder(int orderId, int productId, int quantity) {
        auto it = inventory.find(productId);
        if (it != inventory.end() && it->second.getQuantity() >= quantity) {
            it->second.addQuantity(-quantity);
            orders.insert_or_assign(orderId, Order(productId, quantity, "Shipped"));
            return true;
        }
        return false;
    }

    bool changeOrderStatus(int orderId, const std::string& status) {
        auto it = orders.find(orderId);
        if (it != orders.end()) {
            it->second.setStatus(status);
            return true;
        }
        return false;
    }

    std::optional<std::string> trackOrder(int orderId) const {
        auto it = orders.find(orderId);
        if (it != orders.end()) {
            return it->second.getStatus();
        }
        return std::nullopt;
    }
};