#include <functional>
#include <set>
#include <string>
#include <vector>

struct Customer {
    std::string name;
    int fidelity;
};

struct Item {
    std::string product;
    int quantity;
    double price;
};

class DiscountStrategy {
public:
    using PromoFunc = std::function<double(DiscountStrategy&)>;

    Customer customer;
    std::vector<Item> cart;
    PromoFunc promotion;

    DiscountStrategy(const Customer& customer, const std::vector<Item>& cart, PromoFunc promotion = nullptr)
        : customer(customer), cart(cart), promotion(promotion), m_total(0.0) {
        total();
    }

    double total() {
        m_total = 0.0;
        for (const auto& item : cart) {
            m_total += item.quantity * item.price;
        }
        return m_total;
    }

    double due() {
        double discount = 0.0;
        if (promotion) {
            discount = promotion(*this);
        }
        return m_total - discount;
    }

    static double FidelityPromo(DiscountStrategy& order) {
        if (order.customer.fidelity >= 1000) {
            return order.total() * 0.05;
        }
        return 0.0;
    }

    static double BulkItemPromo(DiscountStrategy& order) {
        double discount = 0.0;
        for (const auto& item : order.cart) {
            if (item.quantity >= 20) {
                discount += item.quantity * item.price * 0.1;
            }
        }
        return discount;
    }

    static double LargeOrderPromo(DiscountStrategy& order) {
        std::set<std::string> products;
        for (const auto& item : order.cart) {
            products.insert(item.product);
        }
        if (products.size() >= 10) {
            return order.total() * 0.07;
        }
        return 0.0;
    }

private:
    double m_total;
};