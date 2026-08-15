#include <vector>
#include <string>
#include <optional>
#include <algorithm>
#include <utility>

class CurrencyConverter {
private:
    std::vector<std::pair<std::string, double>> rates;

    auto find_rate(const std::string& currency) {
        return std::find_if(rates.begin(), rates.end(),
            [&](const std::pair<std::string, double>& p) { return p.first == currency; });
    }

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

    std::optional<double> convert(double amount, const std::string& from_currency, const std::string& to_currency) {
        if (from_currency == to_currency) {
            return amount;
        }

        auto from_it = find_rate(from_currency);
        auto to_it = find_rate(to_currency);

        if (from_it == rates.end() || to_it == rates.end()) {
            return std::nullopt;
        }

        double from_rate = from_it->second;
        double to_rate = to_it->second;

        return (amount / from_rate) * to_rate;
    }

    std::vector<std::string> get_supported_currencies() {
        std::vector<std::string> currencies;
        currencies.reserve(rates.size());
        for (const auto& rate : rates) {
            currencies.push_back(rate.first);
        }
        return currencies;
    }

    std::optional<bool> add_currency_rate(const std::string& currency, double rate) {
        if (find_rate(currency) != rates.end()) {
            return false;
        }
        rates.emplace_back(currency, rate);
        return std::nullopt;
    }

    std::optional<bool> update_currency_rate(const std::string& currency, double new_rate) {
        auto it = find_rate(currency);
        if (it == rates.end()) {
            return false;
        }
        it->second = new_rate;
        return std::nullopt;
    }
};