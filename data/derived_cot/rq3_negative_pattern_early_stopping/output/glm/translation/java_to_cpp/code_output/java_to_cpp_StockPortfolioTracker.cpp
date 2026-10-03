#include <string>
#include <vector>
#include <sstream>
#include <cmath>
#include <functional>

class StockPortfolioTracker {
public:
    class Stock {
    private:
        const std::string name;
        const double price;
        int quantity;

        static int doubleCompare(double a, double b) {
            if (std::isnan(a)) {
                if (std::isnan(b)) return 0;
                return 1;
            }
            if (std::isnan(b)) return -1;
            if (a < b) return -1;
            if (a > b) return 1;
            if (a == 0.0 && b == 0.0) {
                if (std::signbit(a) != std::signbit(b)) {
                    return std::signbit(a) ? -1 : 1;
                }
            }
            return 0;
        }

    public:
        Stock(const std::string& name, double price, int quantity)
            : name(name), price(price), quantity(quantity) {}

        const std::string& getName() const { return name; }
        double getPrice() const { return price; }
        int getQuantity() const { return quantity; }
        void setQuantity(int q) { quantity = q; }

        bool equals(const Stock& other) const {
            return doubleCompare(other.price, price) == 0 &&
                   quantity == other.quantity &&
                   name == other.name;
        }

        int hashCode() const {
            int result = std::hash<std::string>()(name);
            long long priceBits;
            std::memcpy(&priceBits, &price, sizeof(priceBits));
            result = 31 * result + (int)(priceBits ^ (priceBits >> 32));
            result = 31 * result + quantity;
            return result;
        }

        std::string toString() const {
            return name + ": " + std::to_string(quantity) + " shares at $" + std::to_string(price) + " each";
        }
    };

private:
    const double initialCashBalance;
    double cashBalance;
    std::vector<Stock> portfolio;

public:
    StockPortfolioTracker(double initialCashBalance)
        : initialCashBalance(initialCashBalance), cashBalance(initialCashBalance) {}

    void addStock(const Stock& stock) {
        for (auto& s : portfolio) {
            if (s.getName() == stock.getName() && s.getPrice() == stock.getPrice()) {
                s.setQuantity(s.getQuantity() + stock.getQuantity());
                return;
            }
        }
        portfolio.push_back(stock);
    }

    bool removeStock(const Stock& stock) {
        for (size_t i = 0; i < portfolio.size(); i++) {
            if (portfolio[i].getName() == stock.getName() && portfolio[i].getPrice() == stock.getPrice()) {
                if (portfolio[i].getQuantity() >= stock.getQuantity()) {
                    portfolio[i].setQuantity(portfolio[i].getQuantity() - stock.getQuantity());
                    if (portfolio[i].getQuantity() == 0) {
                        portfolio.erase(portfolio.begin() + static_cast<std::ptrdiff_t>(i));
                    }
                    return true;
                }
            }
        }
        return false;
    }

    bool buyStock(const Stock& stock) {
        double cost = stock.getPrice() * stock.getQuantity();
        if (cashBalance >= cost) {
            addStock(stock);
            cashBalance -= cost;
            return true;
        }
        return false;
    }

    bool sellStock(const Stock& stock) {
        double revenue = stock.getPrice() * stock.getQuantity();
        if (removeStock(stock)) {
            cashBalance += revenue;
            return true;
        }
        return false;
    }

    std::vector<Stock> getPortfolio() const {
        return portfolio;
    }

    double getCashBalance() const {
        return cashBalance;
    }

    double calculatePortfolioValue() const {
        double totalValue = 0.0;
        for (const auto& stock : portfolio) {
            totalValue += stock.getPrice() * stock.getQuantity();
        }
        return totalValue;
    }

    std::string getPortfolioSummary() const {
        std::ostringstream summary;
        for (const auto& stock : portfolio) {
            summary << stock.toString() << "\n";
        }
        summary << "Total Value: $" << calculatePortfolioValue() << "\n";
        return summary.str();
    }
};