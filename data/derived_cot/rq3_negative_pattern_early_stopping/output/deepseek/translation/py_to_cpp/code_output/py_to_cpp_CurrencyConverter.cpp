#include <map>
#include <string>
#include <variant>
#include <vector>

class CurrencyConverter {
private:
    std::map<std::string, double> rates;

public:
    CurrencyConverter() {
        rates = {
            {"USD", 1.0},
            {"EUR", 0.85},
            {"GBP", 0.72},
            {"JPY", 110.15},
            {"CAD", 1.23},
            {"AUD", 1.34},
            {"CNY", 6.40}
        };
    }

    // Returns double on success, bool(false) on error.
    std::variant<double, bool> convert(double amount, const std::string& from_currency, const std::string& to_currency) {
        if (from_currency == to_currency) {
            return amount;
        }

        auto from_it = rates.find(from_currency);
        auto to_it = rates.find(to_currency);
        if (from_it == rates.end() || to_it == rates.end()) {
            return false;
        }

        double converted_amount = (amount / from_it->second) * to_it->second;
        return converted_amount;
    }

    std::vector<std::string> get_supported_currencies() {
        std::vector<std::string> currencies;
        currencies.reserve(rates.size());
        for (const auto& pair : rates) {
            currencies.push_back(pair.first);
        }
        return currencies;
    }

    // Returns bool(false) if currency already exists, otherwise adds and returns nothing (void but we mimic Python: returns None on success, False on failure)
    // Python: returns None on success, False on failure.
    // C++: we return bool: false means "unsuccessful", true means "success" (like None but we can't return None)
    // To match exactly: caller should ignore return value on success. We'll use bool where false means error.
    bool add_currency_rate(const std::string& currency, double rate) {
        if (rates.find(currency) != rates.end()) {
            return false; // unsuccessful
        }
        rates[currency] = rate;
        return true; // success
    }

    // Returns bool(false) if currency not found, otherwise updates and returns true.
    bool update_currency_rate(const std::string& currency, double new_rate) {
        if (rates.find(currency) == rates.end()) {
            return false; // unsuccessful
        }
        rates[currency] = new_rate;
        return true; // success
    }
};