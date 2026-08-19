#include <optional>
#include <string>
#include <unordered_map>
#include <utility>

class Warehouse {
private:
    class Product {
    private:
        std::string name;
        int quantity;

    public:
        Product(std::string name, int quantity)
            : name(std::move(name)), quantity(quantity) {}

        void addQuantity(int quantity) {
            this->quantity += quantity;
        }

        int getQuantity() const {
            return quantity;
        }
    };

    class Order {
    private:
        int productId;
        int quantity;
        std::string status;

    public:
        Order(int productId, int quantity, std::string status)
            : productId(productId), quantity(quantity), status(std::move(status)) {}

        std::string getStatus() const {
            return status;
        }

        void setStatus(std::string status) {
            this->status = std::move(status);
        }
    };

    std::unordered_map<int, Product> inventory;
    std::unordered_map<int, Order> orders;

public:
    Warehouse() = default;

    void addProduct(int productId, std::string name, int quantity) {
        auto it = inventory.find(productId);
        if (it != inventory.end()) {
            it->second.addQuantity(quantity);
        } else {
            inventory.emplace(productId, Product(std::move(name), quantity));
        }
    }

    void updateProductQuantity(int productId, int quantity) {
        auto it = inventory.find(productId);
        if (it != inventory.end()) {
            it->second.addQuantity(quantity);
        }
    }

    int getProductQuantity(int productId) {
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

    std::optional<std::string> trackOrder(int orderId) {
        auto it = orders.find(orderId);
        if (it != orders.end()) {
            return it->second.getStatus();
        } else {
            return std::nullopt;
        }
    }
};