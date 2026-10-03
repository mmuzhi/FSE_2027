#include <vector>
#include <string>
#include <utility>

struct Stock {
    std::string name;
    double price;
    int quantity;
};

class StockPortfolioTracker {
private:
    std::vector<Stock> portfolio;
    double cash_balance;

public:
    StockPortfolioTracker(double cash_balance) : cash_balance(cash_balance) {}

    void add_stock(const Stock& stock) {
        for (auto& pf : portfolio) {
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
        double cost = stock.price * stock.quantity;
        if (cost > cash_balance) {
            return false;
        }
        add_stock(stock);
        cash_balance -= cost;
        return true;
    }

    bool sell_stock(const Stock& stock) {
        if (!remove_stock(stock)) {
            return false;
        }
        cash_balance += stock.price * stock.quantity;
        return true;
    }

    double calculate_portfolio_value() const {
        double total = cash_balance;
        for (const auto& stock : portfolio) {
            total += stock.price * stock.quantity;
        }
        return total;
    }

    std::pair<double, std::vector<std::pair<std::string, double>>> get_portfolio_summary() const {
        std::vector<std::pair<std::string, double>> summary;
        for (const auto& stock : portfolio) {
            summary.push_back({stock.name, get_stock_value(stock)});
        }
        double total_value = calculate_portfolio_value();
        return {total_value, summary};
    }

    double get_stock_value(const Stock& stock) const {
        return stock.price * stock.quantity;
    }

    // For testing/debugging (optional)
    const std::vector<Stock>& get_portfolio() const { return portfolio; }
    double get_cash_balance() const { return cash_balance; }
};