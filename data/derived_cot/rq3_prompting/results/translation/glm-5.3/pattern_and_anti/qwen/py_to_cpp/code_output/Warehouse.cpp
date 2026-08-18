#include <string>
#include <optional>
#include <unordered_map>

class Warehouse {
public:
    struct Product {
        std::string name;
        int quantity;
    };

    struct Order {
        int product_id;
        int quantity;
        std::string status;
    };

    void add_product(int product_id, const std::string& name, int quantity) {
        auto it = inventory.find(product_id);
        if (it == inventory.end()) {
            inventory[product_id] = Product{name, quantity};
        } else {
            it->second.quantity += quantity;
        }
    }

    void update_product_quantity(int product_id, int quantity) {
        auto it = inventory.find(product_id);
        if (it != inventory.end()) {
            it->second.quantity += quantity;
        }
    }

    // Returns the quantity, or "False"-like absence via std::nullopt
    std::optional<int> get_product_quantity(int product_id) {
        auto it = inventory.find(product_id);
        if (it != inventory.end()) {
            return it->second.quantity;
        }
        return std::nullopt;
    }

    bool create_order(int order_id, int product_id, int quantity) {
        // Python compares False (== 0) with quantity when product is missing;
        // value_or(0) reproduces that semantics exactly.
        if (get_product_quantity(product_id).value_or(0) >= quantity) {
            update_product_quantity(product_id, -quantity);
            orders[order_id] = Order{product_id, quantity, "Shipped"};
            return true;
        }
        return false;
    }

    bool change_order_status(int order_id, const std::string& status) {
        auto it = orders.find(order_id);
        if (it != orders.end()) {
            it->second.status = status;
            return true;
        }
        return false;
    }

    std::optional<std::string> track_order(int order_id) {
        auto it = orders.find(order_id);
        if (it != orders.end()) {
            return it->second.status;
        }
        return std::nullopt;
    }

private:
    std::unordered_map<int, Product> inventory;  // Product ID: Product
    std::unordered_map<int, Order> orders;       // Order ID: Order
};