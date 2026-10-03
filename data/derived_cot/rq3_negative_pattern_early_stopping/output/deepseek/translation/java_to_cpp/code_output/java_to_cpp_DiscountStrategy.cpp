#include <vector>
#include <string>
#include <functional>
#include <numeric>

class DiscountStrategy;

using Promotion = std::function<double(DiscountStrategy&)>;

class DiscountStrategy {
public:
    static const Promotion FIDELITY_PROMO;
    static const Promotion BULK_ITEM_PROMO;
    static const Promotion LARGE_ORDER_PROMO;

    class Customer {
    private:
        std::string name;
        int fidelity;
    public:
        Customer(const std::string& name, int fidelity) : name(name), fidelity(fidelity) {}
        std::string getName() const { return name; }
        int getFidelity() const { return fidelity; }
    };

    class Product {
    private:
        std::string name;
        int quantity;
        double price;
    public:
        Product(const std::string& name, int quantity, double price) : name(name), quantity(quantity), price(price) {}
        std::string getName() const { return name; }
        int getQuantity() const { return quantity; }
        double getPrice() const { return price; }
    };

    class Cart {
    private:
        std::vector<Product> products;
    public:
        Cart() = default;
        Cart(std::initializer_list<Product> list) : products(list) {}
        void addProduct(const Product& product) { products.push_back(product); }
        std::vector<Product> getProducts() const { return products; }
    };

    DiscountStrategy(Customer customer, Cart cart, const Promotion* promotion)
        : customer(std::move(customer)), cart(std::move(cart)), promotion(promotion) {
        total = calculateTotal();
    }

    double total() const {
        return total;
    }

    double due() {
        double discount = (promotion == nullptr) ? 0.0 : (*promotion)(*this);
        return total - discount;
    }

    double promotion(DiscountStrategy& order) const {
        return (promotion == nullptr) ? 0.0 : (*promotion)(order);
    }

    Customer customer;
    Cart cart;

private:
    const Promotion* promotion;
    double total;

    double calculateTotal() const {
        double sum = 0.0;
        for (const auto& p : cart.getProducts()) {
            sum += p.getQuantity() * p.getPrice();
        }
        return sum;
    }
};

const Promotion DiscountStrategy::FIDELITY_PROMO = [](DiscountStrategy& order) -> double {
    return (order.customer.getFidelity() >= 1000) ? order.total() * 0.05 : 0.0;
};

const Promotion DiscountStrategy::BULK_ITEM_PROMO = [](DiscountStrategy& order) -> double {
    double discount = 0.0;
    for (const auto& item : order.cart.getProducts()) {
        if (item.getQuantity() >= 20) {
            discount += item.getQuantity() * item.getPrice() * 0.1;
        }
    }
    return discount;
};

const Promotion DiscountStrategy::LARGE_ORDER_PROMO = [](DiscountStrategy& order) -> double {
    return (order.cart.getProducts().size() >= 10) ? order.total() * 0.07 : 0.0;
};