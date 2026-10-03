#include <unordered_map>
#include <string>
#include <optional>

struct Product {
    std::string name;
    int quantity;
};

struct Order {
    int product_id;
    int quantity;
    std::string status;
};

class Warehouse {
private:
    std::unordered_map<int, Product> inventory;
    std::unordered_map<int, Order> orders;

public:
    void add_product(int product_id, const std::string& name, int quantity) {
        if (inventory.find(product_id) == inventory.end()) {
            inventory[product_id] = {name, quantity};
        } else {
            inventory[product_id].quantity += quantity;
        }
    }

    void update_product_quantity(int product_id, int quantity) {
        if (inventory.find(product_id) != inventory.end()) {
            inventory[product_id].quantity += quantity;
        }
    }

    std::optional<int> get_product_quantity(int product_id) {
        if (inventory.find(product_id) != inventory.end()) {
            return inventory[product_id].quantity;
        }
        return std::nullopt;
    }

    bool create_order(int order_id, int product_id, int quantity) {
        auto quantity_opt = get_product_quantity(product_id);
        if (!quantity_opt.has_value()) {
            return false;
        }
        if (quantity_opt.value() < quantity) {
            return false;
        }
        update_product_quantity(product_id, -quantity);
        orders[order_id] = {product_id, quantity, "Shipped"};
        return true;
    }

    bool change_order_status(int order_id, const std::string& status) {
        if (orders.find(order_id) == orders.end()) {
            return false;
        }
        orders[order_id].status = status;
        return true;
    }

    std::optional<std::string> track_order(int order_id) {
        if (orders.find(order_id) == orders.end()) {
            return std::nullopt;
        }
        return orders[order_id].status;
    }
};