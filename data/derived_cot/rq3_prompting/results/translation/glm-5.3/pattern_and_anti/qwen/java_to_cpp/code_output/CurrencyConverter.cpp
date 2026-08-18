#pragma once

#include <string>
#include <unordered_map>
#include <unordered_set>

namespace org::example {

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

    double convert(double amount, const std::string& fromCurrency, const std::string& toCurrency) const {
        if (fromCurrency == toCurrency) {
            return amount;
        }

        auto fromIt = rates.find(fromCurrency);
        auto toIt = rates.find(toCurrency);
        if (fromIt == rates.end() || toIt == rates.end()) {
            return -1;
        }

        double fromRate = fromIt->second;
        double toRate = toIt->second;

        double convertedAmount = (amount / fromRate) * toRate;
        return convertedAmount;
    }

    std::unordered_set<std::string> getSupportedCurrencies() const {
        std::unordered_set<std::string> keys;
        for (const auto& entry : rates) {
            keys.insert(entry.first);
        }
        return keys;
    }

    bool addCurrencyRate(const std::string& currency, double rate) {
        if (rates.find(currency) != rates.end()) {
            return false;
        }
        rates[currency] = rate;
        return true;
    }

    bool updateCurrencyRate(const std::string& currency, double newRate) {
        if (rates.find(currency) == rates.end()) {
            return false;
        }
        rates[currency] = newRate;
        return true;
    }

    std::unordered_map<std::string, double>& getRates() {
        return rates;
    }

private:
    std::unordered_map<std::string, double> rates;
};

}  // namespace org::example