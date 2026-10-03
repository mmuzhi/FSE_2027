#include <string>
#include <unordered_map>
#include <unordered_set>

class CurrencyConverter {
private:
    std::unordered_map<std::string, double> rates;

public:
    CurrencyConverter() {
        rates["USD"] = 1.0;
        rates["EUR"] = 0.85;
        rates["GBP"] = 0.72;
        rates["JPY"] = 110.15;
        rates["CAD"] = 1.23;
        rates["AUD"] = 1.34;
        rates["CNY"] = 6.40;
    }

    double convert(double amount, const std::string& fromCurrency, const std::string& toCurrency) {
        if (fromCurrency == toCurrency) {
            return amount;
        }

        auto fromIt = rates.find(fromCurrency);
        auto toIt = rates.find(toCurrency);
        if (fromIt == rates.end() || toIt == rates.end()) {
            return -1.0;
        }

        double fromRate = fromIt->second;
        double toRate = toIt->second;
        double convertedAmount = (amount / fromRate) * toRate;
        return convertedAmount;
    }

    std::unordered_set<std::string> getSupportedCurrencies() const {
        std::unordered_set<std::string> keys;
        for (const auto& pair : rates) {
            keys.insert(pair.first);
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
        auto it = rates.find(currency);
        if (it == rates.end()) {
            return false;
        }
        it->second = newRate;
        return true;
    }

    const std::unordered_map<std::string, double>& getRates() const {
        return rates;
    }
};