#include <string>
#include <vector>
#include <utility>

struct Stock {
    std::string name;
    double price;
    int quantity;
};

struct PortfolioSummaryItem {
    std::string name;
    double value;
};

class StockPortfolioTracker {
public:
    std::vector<Stock> portfolio;
    double cash_balance;

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
        if (stock.price * stock.quantity > cash_balance) {
            return false;
        }
        add_stock(stock);
        cash_balance -= stock.price * stock.quantity;
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

    std::pair<double, std::vector<PortfolioSummaryItem>> get_portfolio_summary() const {
        std::vector<PortfolioSummaryItem> summary;
        for (const auto& stock : portfolio) {
            summary.push_back({stock.name, get_stock_value(stock)});
        }
        double portfolio_value = calculate_portfolio_value();
        return {portfolio_value, summary};
    }

    double get_stock_value(const Stock& stock) const {
        return stock.price * stock.quantity;
    }
};