#include <string>
#include <vector>
#include <utility>
#include <optional>

class CurrencyConverter {
public:
    CurrencyConverter()
        : rates{{"USD", 1.0}, {"EUR", 0.85}, {"GBP", 0.72}, {"JPY", 110.15},
                {"CAD", 1.23}, {"AUD", 1.34}, {"CNY", 6.40}} {}

    // Returns the converted amount, or nullopt when a currency is unsupported
    // (Python returned False in that case). Same-currency conversion returns
    // the amount unchanged even if the currency is unknown.
    std::optional<double> convert(double amount,
                                  const std::string& from_currency,
                                  const std::string& to_currency) const {
        if (from_currency == to_currency) {
            return amount;
        }

        const double* from_rate = find(from_currency);
        const double* to_rate = find(to_currency);

        if (from_rate == nullptr || to_rate == nullptr) {
            return std::nullopt;
        }

        return (amount / *from_rate) * *to_rate;
    }

    // Keys are returned in insertion order (Python 3.7+ dict semantics).
    std::vector<std::string> get_supported_currencies() const {
        std::vector<std::string> currencies;
        currencies.reserve(rates.size());
        for (const auto& entry : rates) {
            currencies.push_back(entry.first);
        }
        return currencies;
    }

    // Returns false if the currency already exists; otherwise adds it
    // (Python returned None on success).
    bool add_currency_rate(const std::string& currency, double rate) {
        if (find(currency) != nullptr) {
            return false;
        }
        rates.emplace_back(currency, rate);
        return true;
    }

    // Returns false if the currency is unknown; otherwise updates its rate
    // (Python returned None on success).
    bool update_currency_rate(const std::string& currency, double new_rate) {
        double* rate = find(currency);
        if (rate == nullptr) {
            return false;
        }
        *rate = new_rate;
        return true;
    }

private:
    // Vector of pairs preserves insertion order, unlike std::map which
    // would reorder keys alphabetically.
    std::vector<std::pair<std::string, double>> rates;

    double* find(const std::string& currency) {
        for (auto& entry : rates) {
            if (entry.first == currency) {
                return &entry.second;
            }
        }
        return nullptr;
    }

    const double* find(const std::string& currency) const {
        for (const auto& entry : rates) {
            if (entry.first == currency) {
                return &entry.second;
            }
        }
        return nullptr;
    }
};