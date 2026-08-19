#include <string>
#include <utility>
#include <vector>
#include <optional>

class CurrencyConverter {
public:
    CurrencyConverter()
        : rates{
              {"USD", 1.0},
              {"EUR", 0.85},
              {"GBP", 0.72},
              {"JPY", 110.15},
              {"CAD", 1.23},
              {"AUD", 1.34},
              {"CNY", 6.40},
          } {}

    // Convert a value between currency types.
    // Returns the converted amount, or no value (Python False) if a currency is unsupported.
    // Note: same-currency conversion returns the amount unchanged, even if unsupported.
    std::optional<double> convert(double amount,
                                  const std::string& from_currency,
                                  const std::string& to_currency) const {
        if (from_currency == to_currency) {
            return amount;
        }

        const double* from_rate = find_rate(from_currency);
        const double* to_rate = find_rate(to_currency);
        if (from_rate == nullptr || to_rate == nullptr) {
            return std::nullopt;  // Python: return False
        }

        return (amount / *from_rate) * *to_rate;
    }

    // Returns all supported currency types in insertion order.
    std::vector<std::string> get_supported_currencies() const {
        std::vector<std::string> currencies;
        currencies.reserve(rates.size());
        for (const auto& entry : rates) {
            currencies.push_back(entry.first);
        }
        return currencies;
    }

    // Add a new currency rate; returns false if the currency already exists,
    // true on success (Python returns None on success, False on failure).
    bool add_currency_rate(const std::string& currency, double rate) {
        if (find_rate(currency) != nullptr) {
            return false;
        }
        rates.emplace_back(currency, rate);
        return true;
    }

    // Update an existing currency rate; returns false if the currency is not supported,
    // true on success (Python returns None on success, False on failure).
    bool update_currency_rate(const std::string& currency, double new_rate) {
        double* rate = find_rate(currency);
        if (rate == nullptr) {
            return false;
        }
        *rate = new_rate;
        return true;
    }

private:
    // Preserves Python dict insertion order (std::map would re-sort keys).
    std::vector<std::pair<std::string, double>> rates;

    const double* find_rate(const std::string& currency) const {
        for (const auto& entry : rates) {
            if (entry.first == currency) {
                return &entry.second;
            }
        }
        return nullptr;
    }

    double* find_rate(const std::string& currency) {
        for (auto& entry : rates) {
            if (entry.first == currency) {
                return &entry.second;
            }
        }
        return nullptr;
    }
};