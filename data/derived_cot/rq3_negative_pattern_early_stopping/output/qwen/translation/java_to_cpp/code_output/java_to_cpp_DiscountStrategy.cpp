#include <vector>
#include <string>
#include <functional>

class Product {
public:
    Product(const std::string& name, int quantity, double price)
        : name(name), quantity(quantity), price(price) {}

    std::string getName() const { return name; }
    int getQuantity() const { return quantity; }
    double getPrice() const { return price; }

private:
    std::string name;
    int quantity;
    double price;
};

class Customer {
public:
    Customer(const std::string& name, int fidelity)
        : name(name), fidelity(fidelity) {}

    std::string getName() const { return name; }
    int getFidelity() const { return fidelity; }

private:
    std::string name;
    int fidelity;
};

class Cart {
public:
    Cart(std::initializer_list<Product> products) {
        for (const auto& product : products) {
            products_.push_back(product);
        }
    }

    void addProduct(const Product& product) {
        products_.push_back(product);
    }

    const std::vector<Product>& getProducts() const {
        return products_;
    }

private:
    std::vector<Product> products_;
};

using Promotion = std::function<double(const DiscountStrategy&)>;

const Promotion FIDELITY_PROMO = [](const DiscountStrategy& order) {
    return order.customer().getFidelity() >= 1000 ? order.total() * 0.05 : 0;
};

const Promotion BULK_ITEM_PROMO = [](const DiscountStrategy& order) {
    double discount = 0;
    for (const auto& item : order.cart().getProducts()) {
        if (item.getQuantity() >= 20) {
            discount += item.getQuantity() * item.getPrice() * 0.1;
        }
    }
    return discount;
};

const Promotion LARGE_ORDER_PROMO = [](const DiscountStrategy& order) {
    return order.cart().getProducts().size() >= 10 ? order.total() * 0.07 : 0;
};

class DiscountStrategy {
private:
    Customer customer;
    Cart cart;
    Promotion promotion;
    mutable double total_value;

    void updateTotal() const {
        total_value = 0;
        for (const auto& item : cart.getProducts()) {
            total_value += item.getQuantity() * item.getPrice();
        }
    }

public:
    DiscountStrategy(const Customer& customer, const Cart& cart, const Promotion& promotion = nullptr)
        : customer(customer), cart(cart), promotion(promotion) {
        updateTotal();
    }

    double total() const {
        updateTotal();
        return total_value;
    }

    double due() const {
        double discount = (promotion == nullptr) ? 0 : promotion(*this);
        return total_value - discount;
    }

    double promotion() const {
        double discount = (promotion == nullptr) ? 0 : promotion(*this);
        return discount;
    }

    const Customer& customer() const { return customer; }
    const Cart& cart() const { return cart; }
};