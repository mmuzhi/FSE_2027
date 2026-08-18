#include <cmath>
#include <iomanip>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

namespace org {
namespace example {

class StockPortfolioTracker {
public:
    class Stock {
    public:
        Stock(std::string name, double price, int quantity)
            : name_(std::move(name)), price_(price), quantity_(quantity) {}

        const std::string& getName() const { return name_; }
        double getPrice() const { return price_; }
        int getQuantity() const { return quantity_; }
        void setQuantity(int quantity) { quantity_ = quantity; }

        // Mimics Java equals(): Double.compare(price, other.price) == 0
        // (NaN == NaN; +0.0 != -0.0), quantity and name equality.
        friend bool operator==(const Stock& lhs, const Stock& rhs) {
            bool priceEqual;
            if (std::isnan(lhs.price_) && std::isnan(rhs.price_)) {
                priceEqual = true;
            } else if (lhs.price_ == rhs.price_) {
                priceEqual = std::signbit(lhs.price_) == std::signbit(rhs.price_);
            } else {
                priceEqual = false;
            }
            return priceEqual && lhs.quantity_ == rhs.quantity_ && lhs.name_ == rhs.name_;
        }

        friend bool operator!=(const Stock& lhs, const Stock& rhs) {
            return !(lhs == rhs);
        }

        std::string toString() const {
            std::ostringstream oss;
            oss << name_ << ": " << quantity_ << " shares at $"
                << doubleToString(price_) << " each";
            return oss.str();
        }

    private:
        const std::string name_;
        const double price_;
        int quantity_;
    };

    explicit StockPortfolioTracker(double initialCashBalance)
        : initialCashBalance_(initialCashBalance),
          cashBalance_(initialCashBalance) {}

    void addStock(const Stock& stock) {
        for (Stock& s : portfolio_) {
            if (s.getName() == stock.getName() && s.getPrice() == stock.getPrice()) {
                s.setQuantity(s.getQuantity() + stock.getQuantity());
                return;
            }
        }
        portfolio_.push_back(stock);
    }

    bool removeStock(const Stock& stock) {
        for (auto it = portfolio_.begin(); it != portfolio_.end(); ++it) {
            if (it->getName() == stock.getName() && it->getPrice() == stock.getPrice()) {
                if (it->getQuantity() >= stock.getQuantity()) {
                    it->setQuantity(it->getQuantity() - stock.getQuantity());
                    if (it->getQuantity() == 0) {
                        portfolio_.erase(it);
                    }
                    return true;
                }
            }
        }
        return false;
    }

    bool buyStock(const Stock& stock) {
        double cost = stock.getPrice() * stock.getQuantity();
        if (cashBalance_ >= cost) {
            addStock(stock);
            cashBalance_ -= cost;
            return true;
        }
        return false;
    }

    bool sellStock(const Stock& stock) {
        double revenue = stock.getPrice() * stock.getQuantity();
        if (removeStock(stock)) {
            cashBalance_ += revenue;
            return true;
        }
        return false;
    }

    std::vector<Stock> getPortfolio() const {
        return portfolio_;
    }

    double getCashBalance() const {
        return cashBalance_;
    }

    double calculatePortfolioValue() const {
        double totalValue = 0.0;
        for (const Stock& stock : portfolio_) {
            totalValue += stock.getPrice() * stock.getQuantity();
        }
        return totalValue;
    }

    std::string getPortfolioSummary() const {
        std::string summary;
        for (const Stock& stock : portfolio_) {
            summary += stock.toString();
            summary += "\n";
        }
        summary += "Total Value: $";
        summary += doubleToString(calculatePortfolioValue());
        summary += "\n";
        return summary;
    }

private:
    // Approximates Java's Double.toString(double) for common values:
    // integral values render with a trailing ".0", non-finite values
    // render as "NaN"/"Infinity"/"-Infinity".
    static std::string doubleToString(double value) {
        if (std::isnan(value)) return "NaN";
        if (std::isinf(value)) return value > 0 ? "Infinity" : "-Infinity";
        std::ostringstream oss;
        oss << std::setprecision(15) << value;
        std::string s = oss.str();
        if (s.find_first_of(".eE") == std::string::npos) {
            s += ".0";
        }
        return s;
    }

    const double initialCashBalance_;
    double cashBalance_;
    std::vector<Stock> portfolio_;
};

} // namespace example
} // namespace org