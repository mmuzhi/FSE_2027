#include <map>
#include <string>
#include <optional>

class Warehouse {
public:
    void add_product(long long product_id, const std::string& name, long long quantity) {
        auto it = inventory.find(product_id);
        if (it == inventory.end()) {
            inventory[product_id] = {name, quantity};
        } else {
            it->second.quantity += quantity;
        }
    }

    void update_product_quantity(long long product_id, long long quantity) {
        auto it = inventory.find(product_id);
        if (it != inventory.end()) {
            it->second.quantity += quantity;
        }
    }

    std::optional<long long> get_product_quantity(long long product_id) const {
        auto it = inventory.find(product_id);
        if (it == inventory.end()) {
            return std::nullopt;
        }
        return it->second.quantity;
    }

    bool create_order(long long order_id, long long product_id, long long quantity) {
        auto qty = get_product_quantity(product_id);
        if (qty.value_or(0) >= quantity) {
            update_product_quantity(product_id, -quantity);
            orders[order_id] = {product_id, quantity, "Shipped"};
            return true;
        }
        return false;
    }

    bool change_order_status(long long order_id, const std::string& status) {
        auto it = orders.find(order_id);
        if (it == orders.end()) {
            return false;
        }
        it->second.status = status;
        return true;
    }

    std::optional<std::string> track_order(long long order_id) const {
        auto it = orders.find(order_id);
        if (it == orders.end()) {
            return std::nullopt;
        }
        return it->second.status;
    }

private:
    struct Product {
        std::string name;
        long long quantity;
    };

    struct Order {
        long long product_id;
        long long quantity;
        std::string status;
    };

    std::map<long long, Product> inventory;
    std::map<long long, Order> orders;
};