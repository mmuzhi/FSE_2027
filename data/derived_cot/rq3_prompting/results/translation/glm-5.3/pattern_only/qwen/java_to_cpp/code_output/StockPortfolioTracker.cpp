#include <algorithm>
#include <charconv>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <string>
#include <utility>
#include <vector>

namespace org {
namespace example {

namespace {

// Emulates Java Double.toString(d) formatting.
std::string javaDoubleToString(double value) {
    if (std::isnan(value)) return "NaN";
    if (std::isinf(value)) return value > 0 ? "Infinity" : "-Infinity";
    if (value == 0.0) return std::signbit(value) ? "-0.0" : "0.0";

    char buf[64];
    auto res = std::to_chars(buf, buf + sizeof(buf), value, std::chars_format::scientific);
    std::string s(buf, res.ptr);

    std::size_t ePos = s.find('e');
    std::string mantissa = s.substr(0, ePos);
    int exp = std::stoi(s.substr(ePos + 1));

    bool negative = (!mantissa.empty() && mantissa[0] == '-');
    if (negative) mantissa.erase(0, 1);
    mantissa.erase(std::remove(mantissa.begin(), mantissa.end(), '.'), mantissa.end());

    const int n = static_cast<int>(mantissa.size());
    const int pointPos = exp + 1;
    std::string out = negative ? "-" : "";

    if (exp >= -3 && exp < 7) {  // decimal form: 1e-3 <= |value| < 1e7
        if (pointPos >= n) {
            out += mantissa + std::string(pointPos - n, '0') + ".0";
        } else if (pointPos > 0) {
            out += mantissa.substr(0, pointPos) + "." + mantissa.substr(pointPos);
        } else {
            out += "0." + std::string(-pointPos, '0') + mantissa;
        }
    } else {  // computerized scientific notation, e.g. "1.0E7", "1.0E-4"
        out += mantissa.substr(0, 1) + ".";
        out += (n > 1) ? mantissa.substr(1) : std::string("0");
        out += "E";
        if (exp < 0) {
            out += "-";
            exp = -exp;
        }
        out += std::to_string(exp);
    }
    return out;
}

// Emulates Double.compare(a, b) == 0 (NaN==NaN, +0.0 != -0.0).
bool javaDoubleEquals(double a, double b) {
    if (std::isnan(a) || std::isnan(b)) return std::isnan(a) && std::isnan(b);
    if (a == b) return a != 0.0 || std::signbit(a) == std::signbit(b);
    return false;
}

// Emulates String.hashCode().
std::uint32_t javaStringHashCode(const std::string& s) {
    std::uint32_t h = 0;
    for (unsigned char c : s) h = 31 * h + c;
    return h;
}

// Emulates Double.hashCode().
std::uint32_t javaDoubleHashCode(double d) {
    std::uint64_t bits;
    if (std::isnan(d)) {
        bits = 0x7ff8000000000000ULL;
    } else {
        std::memcpy(&bits, &d, sizeof(bits));
    }
    return static_cast<std::uint32_t>(bits ^ (bits >> 32));
}

}  // namespace

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

        // Mirrors Java equals(): Double.compare on price, plus quantity and name.
        bool operator==(const Stock& other) const {
            return javaDoubleEquals(other.price_, price_) &&
                   quantity_ == other.quantity_ &&
                   name_ == other.name_;
        }
        bool operator!=(const Stock& other) const { return !(*this == other); }

        // Mirrors Objects.hash(name, price, quantity).
        int hashCode() const {
            std::uint32_t result = 1;
            result = 31 * result + javaStringHashCode(name_);
            result = 31 * result + javaDoubleHashCode(price_);
            result = 31 * result + static_cast<std::uint32_t>(quantity_);
            return static_cast<int>(result);
        }

        std::string toString() const {
            return name_ + ": " + std::to_string(quantity_) + " shares at $" +
                   javaDoubleToString(price_) + " each";
        }

    private:
        const std::string name_;
        const double price_;
        int quantity_;
    };

    StockPortfolioTracker(double initialCashBalance)
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
        summary += javaDoubleToString(calculatePortfolioValue());
        summary += "\n";
        return summary;
    }

private:
    const double initialCashBalance_;
    double cashBalance_;
    std::vector<Stock> portfolio_;
};

}  // namespace example
}  // namespace org