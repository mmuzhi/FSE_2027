#include <vector>
#include <string>
#include <optional>
#include <set>

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
private:
    Customer customer;
    std::vector<CartItem> cart;
    std::optional<double(*)(const DiscountStrategy&)> promotion;
    double total() const;

public:
    DiscountStrategy(const Customer& customer, const std::vector<CartItem>& cart, 
                     std::optional<double(*)(const DiscountStrategy&)> promotion = std::nullopt);

    double due() const;

    static double FidelityPromo(const DiscountStrategy& order);
    static double BulkItemPromo(const DiscountStrategy& order);
    static double LargeOrderPromo(const DiscountStrategy& order);
};

double DiscountStrategy::total() const {
    double sum = 0.0;
    for (const auto& item : cart) {
        sum += item.quantity * item.price;
    }
    return sum;
}

DiscountStrategy::DiscountStrategy(const Customer& customer, const std::vector<CartItem>& cart, 
                     std::optional<double(*)(const DiscountStrategy&)> promotion)
    : customer(customer), cart(cart), promotion(promotion) {
}

double DiscountStrategy::due() const {
    double discount = 0.0;
    if (promotion) {
        discount = (*promotion)(*this);
    }
    return total() - discount;
}

double DiscountStrategy::FidelityPromo(const DiscountStrategy& order) {
    return order.customer.fidelity >= 1000 ? order.total() * 0.05 : 0.0;
}

double DiscountStrategy::BulkItemPromo(const DiscountStrategy& order) {
    double discount = 0.0;
    for (const auto& item : order.cart) {
        if (item.quantity >= 20) {
            discount += item.quantity * item.price * 0.1;
        }
    }
    return discount;
}

double DiscountStrategy::LargeOrderPromo(const DiscountStrategy& order) {
    std::set<std::string> distinct_products;
    for (const auto& item : order.cart) {
        distinct_products.insert(item.product);
    }
    return distinct_products.size() >= 10 ? order.total() * 0.07 : 0.0;
}