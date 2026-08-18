#include <functional>
#include <initializer_list>
#include <string>
#include <utility>
#include <vector>

class DiscountStrategy {
public:
    class Customer {
    public:
        Customer(std::string name, int fidelity)
            : name(std::move(name)), fidelity(fidelity) {}

        const std::string& getName() const { return name; }
        int getFidelity() const { return fidelity; }

    private:
        std::string name;
        int fidelity;
    };

    class Product {
    public:
        Product(std::string name, int quantity, double price)
            : name(std::move(name)), quantity(quantity), price(price) {}

        const std::string& getName() const { return name; }
        int getQuantity() const { return quantity; }
        double getPrice() const { return price; }

    private:
        std::string name;
        int quantity;
        double price;
    };

    class Cart {
    public:
        Cart() = default;

        // Equivalent of the Java varargs constructor Cart(Product...)
        Cart(std::initializer_list<Product> products)
            : products(products.begin(), products.end()) {}

        void addProduct(const Product& product) { products.push_back(product); }

        std::vector<Product>& getProducts() { return products; }
        const std::vector<Product>& getProducts() const { return products; }

    private:
        std::vector<Product> products;
    };

    // Equivalent of the @FunctionalInterface Promotion
    using Promotion = std::function<double(DiscountStrategy&)>;

    static const Promotion FIDELITY_PROMO;
    static const Promotion BULK_ITEM_PROMO;
    static const Promotion LARGE_ORDER_PROMO;

    Customer customer;
    Cart cart;

    DiscountStrategy(Customer customer, Cart cart, Promotion promotion)
        : customer(std::move(customer)),
          cart(std::move(cart)),
          promotion(std::move(promotion)),
          total(0) {
        this->total = this->total();
    }

    double total() {
        total = 0.0;
        for (const Product& p : cart.getProducts()) {
            total += p.getQuantity() * p.getPrice();
        }
        return total;
    }

    double due() {
        double discount = (!promotion) ? 0.0 : promotion(*this);
        return total - discount;
    }

    double promotion(DiscountStrategy& order) {
        (void)order; // unused in the original as well
        return promotion ? promotion(*this) : 0.0;
    }

private:
    Promotion promotion; // renamed: field `promotion` clashes with method in C++
    double total;        // renamed: field `total` clashes with method `total()` in C++
};

// Note: Java permits a field and a method with the same name (`total`,
// `promotion`); C++ does not, so the data members were renamed.
// Behavior is unchanged: the promotion lambdas only use total() and the
// public customer/cart fields.

inline const DiscountStrategy::Promotion DiscountStrategy::FIDELITY_PROMO =
    [](DiscountStrategy& order) {
        return order.customer.getFidelity() >= 1000 ? order.total() * 0.05 : 0.0;
    };

inline const DiscountStrategy::Promotion DiscountStrategy::BULK_ITEM_PROMO =
    [](DiscountStrategy& order) {
        double discount = 0.0;
        for (const Product& item : order.cart.getProducts()) {
            if (item.getQuantity() >= 20) {
                discount += item.getQuantity() * item.getPrice() * 0.1;
            }
        }
        return discount;
    };

inline const DiscountStrategy::Promotion DiscountStrategy::LARGE_ORDER_PROMO =
    [](DiscountStrategy& order) {
        return order.cart.getProducts().size() >= 10 ? order.total() * 0.07 : 0.0;
    };