#include <string>
#include <utility>
#include <vector>

class StockPortfolioTracker {
public:
    // Mirrors the Python stock dict with keys "name", "price", "quantity".
    struct Stock {
        std::string name;
        double price;
        int quantity;
    };

    StockPortfolioTracker(double cash_balance) : cash_balance(cash_balance) {
        // portfolio starts empty
    }

    void add_stock(const Stock& stock) {
        for (Stock& pf : portfolio) {
            if (pf.name == stock.name) {
                pf.quantity += stock.quantity;
                return;
            }
        }
        portfolio.push_back(stock);
    }

    bool remove_stock(const Stock& stock) {
        for (auto it = portfolio.begin(); it != portfolio.end(); ++it) {
            if (it->name == stock.name && it->quantity >= stock.quantity) {
                it->quantity -= stock.quantity;
                if (it->quantity == 0) {
                    portfolio.erase(it);
                }
                return true;
            }
        }
        return false;
    }

    bool buy_stock(const Stock& stock) {
        if (stock.price * stock.quantity > cash_balance) {
            return false;
        } else {
            add_stock(stock);
            cash_balance -= stock.price * stock.quantity;
            return true;
        }
    }

    bool sell_stock(const Stock& stock) {
        if (!remove_stock(stock)) {
            return false;
        }
        cash_balance += stock.price * stock.quantity;
        return true;
    }

    double calculate_portfolio_value() const {
        double total_value = cash_balance;
        for (const Stock& stock : portfolio) {
            total_value += stock.price * stock.quantity;
        }
        return total_value;
    }

    std::pair<double, std::vector<std::pair<std::string, double>>> get_portfolio_summary() const {
        std::vector<std::pair<std::string, double>> summary;
        for (const Stock& stock : portfolio) {
            double value = get_stock_value(stock);
            summary.emplace_back(stock.name, value);
        }
        double portfolio_value = calculate_portfolio_value();
        return {portfolio_value, summary};
    }

    double get_stock_value(const Stock& stock) const {
        return stock.price * stock.quantity;
    }

    std::vector<Stock> portfolio;
    double cash_balance;
};