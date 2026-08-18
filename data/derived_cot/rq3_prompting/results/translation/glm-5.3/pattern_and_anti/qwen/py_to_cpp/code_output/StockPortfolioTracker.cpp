#include <string>
#include <vector>
#include <utility>

class StockPortfolioTracker {
public:
    struct Stock {
        std::string name;
        double price;
        int quantity;
    };

    struct StockValue {
        std::string name;
        double value;
    };

    std::vector<Stock> portfolio;
    double cash_balance;

    explicit StockPortfolioTracker(double cash_balance)
        : cash_balance(cash_balance) {}

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
        if (stock.price * stock.quantity > cash_balance) {
            return false;
        } else {
            add_stock(stock);
            cash_balance -= stock.price * stock.quantity;
            return true;
        }
    }

    bool sell_stock(const Stock& stock) {
        if (remove_stock(stock) == false) {
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

    std::pair<double, std::vector<StockValue>> get_portfolio_summary() const {
        std::vector<StockValue> summary;
        for (const auto& stock : portfolio) {
            double value = get_stock_value(stock);
            summary.push_back({stock.name, value});
        }
        double portfolio_value = calculate_portfolio_value();
        return {portfolio_value, summary};
    }

    double get_stock_value(const Stock& stock) const {
        return stock.price * stock.quantity;
    }
};