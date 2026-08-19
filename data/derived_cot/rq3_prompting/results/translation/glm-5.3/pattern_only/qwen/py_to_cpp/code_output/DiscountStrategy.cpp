#include <set>
#include <string>
#include <utility>
#include <vector>

class DiscountStrategy {
public:
    struct Customer {
        std::string name;
        double fidelity;
    };

    struct CartItem {
        std::string product;
        int quantity;
        double price;
    };

    // Python: promotion is a plain function (static method) or None
    using Promotion = double (*)(DiscountStrategy&);

    DiscountStrategy(Customer customer, std::vector<CartItem> cart, Promotion promotion = nullptr)
        : customer_(std::move(customer)),
          cart_(std::move(cart)),
          promotion_(promotion) {
        total_ = total();
    }

    double total() {
        double sum = 0.0;
        for (const CartItem& item : cart_) {
            sum += item.quantity * item.price;
        }
        total_ = sum;
        return total_;
    }

    double due() {
        double discount;
        if (promotion_ == nullptr) {
            discount = 0;
        } else {
            discount = promotion_(*this);
        }
        return total_ - discount;
    }

    static double FidelityPromo(DiscountStrategy& order) {
        return order.customer_.fidelity >= 1000 ? order.total() * 0.05 : 0;
    }

    static double BulkItemPromo(DiscountStrategy& order) {
        double discount = 0;
        for (const CartItem& item : order.cart_) {
            if (item.quantity >= 20) {
                discount += item.quantity * item.price * 0.1;
            }
        }
        return discount;
    }

    static double LargeOrderPromo(DiscountStrategy& order) {
        std::set<std::string> distinct_products;
        for (const CartItem& item : order.cart_) {
            distinct_products.insert(item.product);
        }
        return distinct_products.size() >= 10 ? order.total() * 0.07 : 0;
    }

private:
    Customer customer_;
    std::vector<CartItem> cart_;
    Promotion promotion_;
    double total_;  // maps to Python's name-mangled __total
};