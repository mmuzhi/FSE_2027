#include <string>
#include <vector>
#include <unordered_set>
#include <numeric>

struct Customer {
    std::string name;
    int fidelity;
};

struct CartItem {
    std::string product;
    int quantity;
    double price;
};

class DiscountStrategy {
public:
    // Type for promotion function pointers (static methods)
    using PromoFunc = double (*)(DiscountStrategy&);

    // Constructor
    DiscountStrategy(Customer customer, std::vector<CartItem> cart, PromoFunc promotion = nullptr)
        : customer_(std::move(customer))
        , cart_(std::move(cart))
        , promotion_(promotion)
    {
        total();  // initialize total_
    }

    // Recalculate total cost and return it
    double total() {
        total_ = 0.0;
        for (const auto& item : cart_) {
            total_ += static_cast<double>(item.quantity) * item.price;
        }
        return total_;
    }

    // Final amount to pay after applying discount
    double due() {
        double discount = 0.0;
        if (promotion_ != nullptr) {
            discount = promotion_(*this);  // promotion may call total() and update total_
        }
        return total_ - discount;
    }

    // --- Static promotion functions ---
    static double FidelityPromo(DiscountStrategy& order) {
        if (order.customer_.fidelity >= 1000) {
            return order.total() * 0.05;
        }
        return 0.0;
    }

    static double BulkItemPromo(DiscountStrategy& order) {
        double discount = 0.0;
        for (const auto& item : order.cart_) {
            if (item.quantity >= 20) {
                discount += static_cast<double>(item.quantity) * item.price * 0.1;
            }
        }
        return discount;
    }

    static double LargeOrderPromo(DiscountStrategy& order) {
        std::unordered_set<std::string> distinct_products;
        for (const auto& item : order.cart_) {
            distinct_products.insert(item.product);
        }
        if (distinct_products.size() >= 10) {
            return order.total() * 0.07;
        }
        return 0.0;
    }

private:
    Customer customer_;
    std::vector<CartItem> cart_;
    double total_ = 0.0;
    PromoFunc promotion_ = nullptr;
};