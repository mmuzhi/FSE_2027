#include <optional>
#include <string>
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

    // Product ID: Product
    std::unordered_map<int, Product> inventory;
    // Order ID: Order
    std::unordered_map<int, Order> orders;

    // Add a product to the inventory. If it already exists, add `quantity`
    // to the existing quantity; otherwise insert it as a new product.
    void add_product(int product_id, const std::string& name, int quantity) {
        auto it = inventory.find(product_id);
        if (it == inventory.end()) {
            inventory.emplace(product_id, Product{name, quantity});
        } else {
            it->second.quantity += quantity;
        }
    }

    // Add `quantity` to the product's quantity if the product exists;
    // otherwise do nothing.
    void update_product_quantity(int product_id, int quantity) {
        auto it = inventory.find(product_id);
        if (it != inventory.end()) {
            it->second.quantity += quantity;
        }
    }

    // Return the quantity of the product, or std::nullopt (Python's False)
    // if the product_id is not in the inventory.
    std::optional<int> get_product_quantity(int product_id) const {
        auto it = inventory.find(product_id);
        if (it != inventory.end()) {
            return it->second.quantity;
        }
        return std::nullopt;
    }

    // Create an order with default status "Shipped" and put it into `orders`
    // if the available quantity is adequate. Returns false when the order
    // cannot be created (Python's `return False`); returns true on success
    // (Python implicitly returns None on success).
    //
    // Note: a missing product behaves like quantity 0, matching Python where
    // `False >= quantity` is evaluated as `0 >= quantity`.
    bool create_order(int order_id, int product_id, int quantity) {
        if (get_product_quantity(product_id).value_or(0) >= quantity) {
            update_product_quantity(product_id, -quantity);  // no-op if missing
            orders[order_id] = Order{product_id, quantity, "Shipped"};
            return true;
        }
        return false;
    }

    // Change the status of the order if order_id exists in orders.
    // Returns false only if the order_id is not in orders
    // (true on success, where Python implicitly returns None).
    bool change_order_status(int order_id, const std::string& status) {
        auto it = orders.find(order_id);
        if (it != orders.end()) {
            it->second.status = status;
            return true;
        }
        return false;
    }

    // Return the status of the order, or std::nullopt (Python's False)
    // if the order_id is not in orders.
    std::optional<std::string> track_order(int order_id) const {
        auto it = orders.find(order_id);
        if (it != orders.end()) {
            return it->second.status;
        }
        return std::nullopt;
    }
};