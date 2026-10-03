#include <string>
#include <unordered_map>
#include <variant>

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
public:
    std::unordered_map<int, Product> inventory;
    std::unordered_map<int, Order> orders;

    void add_product(int product_id, const std::string& name, int quantity) {
        auto it = inventory.find(product_id);
        if (it == inventory.end()) {
            inventory[product_id] = {name, quantity};
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

    std::variant<int, bool> get_product_quantity(int product_id) {
        auto it = inventory.find(product_id);
        if (it != inventory.end()) {
            return it->second.quantity;
        }
        return false;
    }

    std::variant<std::monostate, bool> create_order(int order_id, int product_id, int quantity) {
        auto pq = get_product_quantity(product_id);
        int qty = std::holds_alternative<int>(pq) ? std::get<int>(pq) : 0;
        if (qty >= quantity) {
            update_product_quantity(product_id, -quantity);
            orders[order_id] = {product_id, quantity, "Shipped"};
            return std::monostate{};
        }
        return false;
    }

    std::variant<std::monostate, bool> change_order_status(int order_id, const std::string& status) {
        auto it = orders.find(order_id);
        if (it != orders.end()) {
            it->second.status = status;
            return std::monostate{};
        }
        return false;
    }

    std::variant<std::string, bool> track_order(int order_id) {
        auto it = orders.find(order_id);
        if (it != orders.end()) {
            return it->second.status;
        }
        return false;
    }
};