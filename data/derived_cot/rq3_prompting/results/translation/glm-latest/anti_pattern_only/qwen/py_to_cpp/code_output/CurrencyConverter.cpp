#include <optional>
#include <string>
#include <utility>
#include <vector>

/**
 * A class for currency conversion, which supports converting amounts between
 * different currencies, retrieving supported currencies, adding new currency
 * rates, and updating existing currency rates.
 */
class CurrencyConverter {
public:
    // Initialize the exchange rate of the US dollar against various currencies.
    // A vector of pairs preserves insertion order exactly like a Python dict,
    // which matters for get_supported_currencies() and for the position of
    // currencies added later.
    CurrencyConverter()
        : rates({
              {"USD", 1.0},
              {"EUR", 0.85},
              {"GBP", 0.72},
              {"JPY", 110.15},
              {"CAD", 1.23},
              {"AUD", 1.34},
              {"CNY", 6.40},
          }) {}

    /**
     * Convert the value of a given currency to another currency type.
     * Returns the converted amount, or std::nullopt when either currency is
     * not supported (the Python version returns False in that case).
     */
    std::optional<double> convert(double amount,
                                  const std::string& from_currency,
                                  const std::string& to_currency) const {
        if (from_currency == to_currency) {
            return amount;
        }

        const double* from_rate = find_rate(from_currency);
        const double* to_rate = find_rate(to_currency);
        if (from_rate == nullptr || to_rate == nullptr) {
            return std::nullopt;
        }

        return (amount / *from_rate) * *to_rate;
    }

    /**
     * Returns a list of supported currency types, in insertion order
     * (matching Python dict key ordering).
     */
    std::vector<std::string> get_supported_currencies() const {
        std::vector<std::string> currencies;
        currencies.reserve(rates.size());
        for (const auto& entry : rates) {
            currencies.push_back(entry.first);
        }
        return currencies;
    }

    /**
     * Add a new supported currency type.
     * Returns false if the currency type is already in the support list
     * (the Python version returns False on failure and None on success).
     */
    bool add_currency_rate(const std::string& currency, double rate) {
        if (find_rate(currency) != nullptr) {
            return false;
        }
        rates.emplace_back(currency, rate);
        return true;
    }

    /**
     * Update the exchange rate for a certain currency.
     * Returns false if the currency is not supported (the Python version
     * returns False on failure and None on success).
     */
    bool update_currency_rate(const std::string& currency, double new_rate) {
        double* rate = find_rate(currency);
        if (rate == nullptr) {
            return false;
        }
        *rate = new_rate;
        return true;
    }

private:
    // Preserves insertion order, mirroring the Python dict.
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