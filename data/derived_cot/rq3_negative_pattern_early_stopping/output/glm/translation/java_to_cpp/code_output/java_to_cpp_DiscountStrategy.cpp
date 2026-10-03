#include <functional>
#include <vector>
#include <string>

class DiscountStrategy {
public:
    class Customer {
    private:
        std::string name;
        int fidelity;
    public:
        Customer(std::string name, int fidelity) : name(std::move(name)), fidelity(fidelity) {}
        std::string getName() const { return name; }
        int getFidelity() const { return fidelity; }
    };

    class Product {
    private:
        std::string name;
        int quantity;
        double price;
    public:
        Product(std::string name, int quantity, double price) : name(std::move(name)), quantity(quantity), price(price) {}
        std::string getName() const { return name; }
        int getQuantity() const { return quantity; }
        double getPrice() const { return price; }
    };

    class Cart {
    private:
        std::vector<Product> products;
    public:
        Cart() = default;
        Cart(std::initializer_list<Product> prods) : products(prods) {}
        void addProduct(const Product& product) { products.push_back(product); }
        std::vector<Product>& getProducts() { return products; }
    };

    using Promotion = std::function<double(DiscountStrategy&)>;

    static Promotion FIDELITY_PROMO;
    static Promotion BULK_ITEM_PROMO;
    static Promotion LARGE_ORDER_PROMO;

    Customer customer;
    Cart cart;
    Promotion promotion_;
    double total;

    DiscountStrategy(Customer customer, Cart cart, Promotion promotion)
        : customer(std::move(customer)), cart(std::move(cart)), promotion_(std::move(promotion)), total(0) {
        this->total = total();
    }

    double total() {
        total = 0;
        for (const auto& p : cart.getProducts()) {
            total += p.getQuantity() * p.getPrice();
        }
        return total;
    }

    double due() {
        double discount = promotion_ ? promotion_(*this) : 0;
        return total - discount;
    }

    double promotion(DiscountStrategy& order) {
        return promotion_ ? promotion_(*this) : 0;
    }
};

DiscountStrategy::Promotion DiscountStrategy::FIDELITY_PROMO = [](DiscountStrategy& order) -> double {
    return order.customer.getFidelity() >= 1000 ? order.total() * 0.05 : 0;
};

DiscountStrategy::Promotion DiscountStrategy::BULK_ITEM_PROMO = [](DiscountStrategy& order) -> double {
    double discount = 0;
    for (const auto& item : order.cart.getProducts()) {
        if (item.getQuantity() >= 20) {
            discount += item.getQuantity() * item.getPrice() * 0.1;
        }
    }
    return discount;
};

DiscountStrategy::Promotion DiscountStrategy::LARGE_ORDER_PROMO = [](DiscountStrategy& order) -> double {
    return order.cart.getProducts().size() >= 10 ? order.total() * 0.07 : 0;
};