#include <functional>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

class DiscountStrategy {
public:
    struct Customer {
        std::string name;
        double fidelity;  // fidelity points
    };

    struct Item {
        std::string product;
        int quantity;
        double price;
    };

    // Promotion: a function taking the order and returning the discount amount.
    using Promotion = std::function<double(DiscountStrategy&)>;

    DiscountStrategy(Customer customer, std::vector<Item> cart,
                     Promotion promotion = nullptr)
        : customer_(std::move(customer)),
          cart_(std::move(cart)),
          promotion_(std::move(promotion)) {
        total_ = total();
    }

    // Recomputes (and caches) the total cost of items in the cart.
    double total() {
        total_ = 0.0;
        for (const Item& item : cart_) {
            total_ += item.quantity * item.price;
        }
        return total_;
    }

    // Final amount to be paid after applying the discount.
    double due() {
        double discount = 0.0;
        if (promotion_) {
            discount = promotion_(*this);
        }
        return total_ - discount;
    }

    // 5% discount on the whole order for customers with >= 1000 fidelity points.
    static double FidelityPromo(DiscountStrategy& order) {
        return order.customer_.fidelity >= 1000 ? order.total() * 0.05 : 0.0;
    }

    // 10% discount on each item whose quantity reaches 20 or more.
    static double BulkItemPromo(DiscountStrategy& order) {
        double discount = 0.0;
        for (const Item& item : order.cart_) {
            if (item.quantity >= 20) {
                discount += item.quantity * item.price * 0.1;
            }
        }
        return discount;
    }

    // 7% discount on the entire order if there are >= 10 distinct products.
    static double LargeOrderPromo(DiscountStrategy& order) {
        std::unordered_set<std::string> products;
        for (const Item& item : order.cart_) {
            products.insert(item.product);
        }
        return products.size() >= 10 ? order.total() * 0.07 : 0.0;
    }

private:
    Customer customer_;
    std::vector<Item> cart_;
    Promotion promotion_;
    double total_ = 0.0;
};