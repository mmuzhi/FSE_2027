#include <map>
#include <string>
#include <optional>

class Warehouse {
public:
    Warehouse() = default;

    void add_product(int product_id, const std::string& name, int quantity) {
        auto it = inventory_.find(product_id);
        if (it != inventory_.end()) {
            it->second.quantity += quantity;
        } else {
            inventory_[product_id] = {name, quantity};
        }
    }

    void update_product_quantity(int product_id, int quantity) {
        auto it = inventory_.find(product_id);
        if (it != inventory_.end()) {
            it->second.quantity += quantity;
        }
    }

    int get_product_quantity(int product_id) const {
        auto it = inventory_.find(product_id);
        if (it != inventory_.end()) {
            return it->second.quantity;
        }
        return 0;  // mimics Python's False (0) when product not found
    }

    bool create_order(int order_id, int product_id, int quantity) {
        if (get_product_quantity(product_id) >= quantity) {
            update_product_quantity(product_id, -quantity);
            orders_[order_id] = {product_id, quantity, "Shipped"};
            return true;  // success
        }
        return false;  // failure
    }

    bool change_order_status(int order_id, const std::string& status) {
        auto it = orders_.find(order_id);
        if (it != orders_.end()) {
            it->second.status = status;
            return true;  // success
        }
        return false;  // order not found
    }

    std::optional<std::string> track_order(int order_id) const {
        auto it = orders_.find(order_id);
        if (it != orders_.end()) {
            return it->second.status;
        }
        return std::nullopt;  // mimics Python's False for not found
    }

private:
    struct Product {
        std::string name;
        int quantity;
    };

    struct Order {
        int product_id;
        int quantity;
        std::string status;
    };

    std::map<int, Product> inventory_;
    std::map<int, Order> orders_;
};