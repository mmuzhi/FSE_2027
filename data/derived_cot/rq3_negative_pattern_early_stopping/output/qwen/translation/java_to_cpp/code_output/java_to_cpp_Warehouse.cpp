#include <iostream>
#include <map>
#include <string>
#include <unordered_map>

class Warehouse {
private:
    using ProductMap = std::unordered_map<int, Product>;
    using OrderMap = std::unordered_map<int, Order>;

    ProductMap inventory;
    OrderMap orders;

    class Product {
    public:
        Product(const std::string& name, int quantity) : name(name), quantity(quantity) {}

        void addQuantity(int quantity) {
            this->quantity += quantity;
        }

        int getQuantity() const {
            return quantity;
        }

    private:
        std::string name;
        int quantity;
    };

    class Order {
    public:
        Order(int productId, int quantity, const std::string& status) : productId(productId), quantity(quantity), status(status) {}

        void setStatus(const std::string& status) {
            this->status = status;
        }

        std::string getStatus() const {
            return status;
        }

    private:
        int productId;
        int quantity;
        std::string status;
    };

public:
    Warehouse() : inventory(), orders() {}

    void addProduct(int productId, const std::string& name, int quantity) {
        auto it = inventory.find(productId);
        if (it != inventory.end()) {
            it->second.addQuantity(quantity);
        } else {
            inventory[productId] = Product(name, quantity);
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
        auto productIt = inventory.find(productId);
        if (productIt != inventory.end()) {
            if (productIt->second.getQuantity() >= quantity) {
                productIt->second.addQuantity(-quantity);
                orders[orderId] = Order(productId, quantity, "Shipped");
                return true;
            }
        }
        return false;
    }

    bool changeOrderStatus(int orderId, const std::string& status) {
        auto orderIt = orders.find(orderId);
        if (orderIt != orders.end()) {
            orderIt->second.setStatus(status);
            return true;
        }
        return false;
    }

    std::string trackOrder(int orderId) {
        auto orderIt = orders.find(orderId);
        if (orderIt != orders.end()) {
            return orderIt->second.getStatus();
        } else {
            return nullptr;
        }
    }
};