#include <functional>
#include <initializer_list>
#include <string>
#include <type_traits>
#include <utility>
#include <vector>

namespace org {
namespace example {

class DiscountStrategy {
public:
    class Customer {
    private:
        std::string name;
        int fidelity;

    public:
        Customer(std::string name, int fidelity) : name(std::move(name)), fidelity(fidelity) {}

        const std::string& getName() const { return name; }
        int getFidelity() const { return fidelity; }
    };

    class Product {
    private:
        std::string name;
        int quantity;
        double price;

    public:
        Product(std::string name, int quantity, double price)
            : name(std::move(name)), quantity(quantity), price(price) {}

        const std::string& getName() const { return name; }
        int getQuantity() const { return quantity; }
        double getPrice() const { return price; }
    };

    class Cart {
    private:
        std::vector<Product> products;

    public:
        Cart() = default;

        Cart(std::initializer_list<Product> init) : products(init) {}

        template<typename... Args>
        Cart(const Args&... args) {
            static_assert((std::is_same_v<Args, Product> && ...),
                          "All arguments must be Product");
            (products.push_back(args), ...);
        }

        void addProduct(const Product& product) {
            products.push_back(product);
        }

        std::vector<Product>& getProducts() { return products; }
        const std::vector<Product>& getProducts() const { return products; }
    };

    using Promotion = std::function<double(DiscountStrategy&)>;

private:
    const Customer* customer_;
    const Cart* cart_;
    Promotion promotion_;
    double total_ = 0.0;

public:
    double total();

    static inline const Promotion FIDELITY_PROMO = [](DiscountStrategy& order) -> double {
        return order.customer_->getFidelity() >= 1000 ? order.total() * 0.05 : 0;
    };

    static inline const Promotion BULK_ITEM_PROMO = [](DiscountStrategy& order) -> double {
        double discount = 0;
        for (const auto& item : order.cart_->getProducts()) {
            if (item.getQuantity() >= 20) {
                discount += item.getQuantity() * item.getPrice() * 0.1;
            }
        }
        return discount;
    };

    static inline const Promotion LARGE_ORDER_PROMO = [](DiscountStrategy& order) -> double {
        return order.cart_->getProducts().size() >= 10 ? order.total() * 0.07 : 0;
    };

    DiscountStrategy(Customer& customer, Cart& cart, Promotion promotion)
        : customer_(&customer), cart_(&cart), promotion_(std::move(promotion)) {
        total_ = total();
    }

    double total() {
        double sum = 0;
        for (const auto& p : cart_->getProducts()) {
            sum += p.getQuantity() * p.getPrice();
        }
        total_ = sum;
        return total_;
    }

    double due() {
        double discount = promotion_ ? promotion_(*this) : 0;
        return total_ - discount;
    }

    double promotion(const DiscountStrategy&) {
        return promotion_ ? promotion_(*this) : 0;
    }
};

} // namespace example
} // namespace org