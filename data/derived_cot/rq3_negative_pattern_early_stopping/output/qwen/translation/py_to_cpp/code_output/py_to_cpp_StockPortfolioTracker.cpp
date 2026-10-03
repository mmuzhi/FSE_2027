#include <vector>
#include <string>

struct Stock {
    std::string name;
    double price;
    int quantity;
};

class StockPortfolioTracker {
public:
    StockPortfolioTracker(double cash_balance) : cash_balance(cash_balance) {}

    bool add_stock(const Stock& stock) {
        for (auto& existing : portfolio) {
            if (existing.name == stock.name) {
                existing.quantity += stock.quantity;
                return true;
            }
        }
        portfolio.push_back(stock);
        return true;
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
        double total_cost = stock.price * stock.quantity;
        if (total_cost > cash_balance) {
            return false;
        }
        add_stock(stock);
        cash_balance -= total_cost;
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
        double total_value = cash_balance;
        for (const auto& stock : portfolio) {
            total_value += stock.price * stock.quantity;
        }
        return total_value;
    }

    std::pair<double, std::vector<std::pair<std::string, double>>> get_portfolio_summary() const {
        std::vector<std::pair<std::string, double>> summary;
        for (const auto& stock : portfolio) {
            double value = stock.price * stock.quantity;
            summary.push_back({stock.name, value});
        }
        return {calculate_portfolio_value(), summary};
    }

    double get_stock_value(const Stock& stock) const {
        return stock.price * stock.quantity;
    }

private:
    std::vector<Stock> portfolio;
    double cash_balance;
};