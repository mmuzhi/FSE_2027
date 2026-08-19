#include <string>
#include <unordered_map>
#include <optional>

// The class manages inventory and orders, including adding products,
// updating product quantities, retrieving product quantities, creating
// orders, changing order statuses, and tracking orders.
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

    Warehouse() = default;

    // Add product to inventory; if it already exists, add to its quantity.
    void add_product(int product_id, const std::string& name, int quantity) {
        auto it = inventory.find(product_id);
        if (it == inventory.end()) {
            inventory[product_id] = Product{name, quantity};
        } else {
            it->second.quantity += quantity;
        }
    }

    // Add `quantity` (delta, may be negative) to the product if it exists.
    void update_product_quantity(int product_id, int quantity) {
        auto it = inventory.find(product_id);
        if (it != inventory.end()) {
            it->second.quantity += quantity;
        }
    }

    // Return the product's quantity, or "false" (nullopt) if not in inventory.
    // Note: Python's False compares as 0 numerically; use .value_or(0)
    // wherever Python would use the result in a numeric comparison.
    std::optional<int> get_product_quantity(int product_id) const {
        auto it = inventory.find(product_id);
        if (it != inventory.end()) {
            return it->second.quantity;
        }
        return std::nullopt;  // Python: False
    }

    // Create an order with default status "Shipped" and deduct the quantity
    // from inventory. Returns false only if the product is missing or the
    // quantity is inadequate (missing product compares as 0, like Python's
    // False). Returns true on success (Python returns None).
    bool create_order(int order_id, int product_id, int quantity) {
        if (get_product_quantity(product_id).value_or(0) >= quantity) {
            update_product_quantity(product_id, -quantity);
            orders[order_id] = Order{product_id, quantity, "Shipped"};
            return true;   // Python: None
        }
        return false;
    }

    // Change the status of an existing order.
    // Returns false only if order_id is not in orders (Python: False);
    // returns true on success (Python: None).
    bool change_order_status(int order_id, const std::string& status) {
        auto it = orders.find(order_id);
        if (it != orders.end()) {
            it->second.status = status;
            return true;   // Python: None
        }
        return false;
    }

    // Return the order's status, or "false" (nullopt) if not in orders.
    std::optional<std::string> track_order(int order_id) const {
        auto it = orders.find(order_id);
        if (it != orders.end()) {
            return it->second.status;
        }
        return std::nullopt;  // Python: False
    }

private:
    std::unordered_map<int, Product> inventory;  // Product ID: Product
    std::unordered_map<int, Order> orders;       // Order ID: Order
};