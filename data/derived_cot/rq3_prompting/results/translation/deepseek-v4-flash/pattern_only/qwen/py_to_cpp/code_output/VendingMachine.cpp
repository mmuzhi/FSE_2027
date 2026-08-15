#include <string>
#include <unordered_map>
#include <vector>
#include <variant>
#include <charconv>
#include <cmath>
#include <cstdlib>

class VendingMachine {
private:
    struct Item {
        double price;
        int quantity;
    };

    std::unordered_map<std::string, Item> inventory;
    std::vector<std::string> order;
    double balance;

    static std::string format_double(double value) {
        if (std::isnan(value)) return "nan";
        if (std::isinf(value)) return std::signbit(value) ? "-inf" : "inf";

        bool neg = std::signbit(value);
        if (value == 0.0) {
            return neg ? "-0.0" : "0.0";
        }
        if (neg) value = -value;

        char buf[128];
        auto res = std::to_chars(buf, buf + sizeof(buf), value, std::chars_format::scientific);
        std::string sci(buf, res.ptr);

        size_t epos = sci.find('e');
        std::string mant = sci.substr(0, epos);
        int exp = std::stoi(sci.substr(epos + 1));

        std::string digits;
        for (char c : mant) {
            if (c != '.') digits += c;
        }
        while (digits.size() > 1 && digits.back() == '0') {
            digits.pop_back();
        }

        std::string out;
        if (neg) out += '-';

        if (exp >= -4 && exp < 16) {
            if (exp >= 0) {
                int point_pos = exp + 1;
                if (digits.size() > static_cast<size_t>(point_pos)) {
                    out += digits.substr(0, point_pos);
                    out += ".";
                    out += digits.substr(point_pos);
                } else {
                    out += digits;
                    out.append(static_cast<size_t>(point_pos) - digits.size(), '0');
                    out += ".0";
                }
            } else {
                out += "0.";
                out.append(static_cast<size_t>(-exp - 1), '0');
                out += digits;
            }
        } else {
            out += digits[0];
            if (digits.size() > 1) {
                out += ".";
                out += digits.substr(1);
            }
            out += 'e';
            if (exp >= 0) out += '+';
            else out += '-';
            int abs_exp = std::abs(exp);
            if (abs_exp < 10) out += '0';
            out += std::to_string(abs_exp);
        }
        return out;
    }

public:
    VendingMachine() : balance(0.0) {}

    void add_item(const std::string& item_name, double price, int quantity) {
        if (!restock_item(item_name, quantity)) {
            inventory[item_name] = {price, quantity};
            order.push_back(item_name);
        }
    }

    double insert_coin(double amount) {
        balance += amount;
        return balance;
    }

    std::variant<double, bool> purchase_item(const std::string& item_name) {
        auto it = inventory.find(item_name);
        if (it != inventory.end()) {
            Item& item = it->second;
            if (item.quantity > 0 && balance >= item.price) {
                balance -= item.price;
                item.quantity -= 1;
                return balance;
            } else {
                return false;
            }
        } else {
            return false;
        }
    }

    bool restock_item(const std::string& item_name, int quantity) {
        auto it = inventory.find(item_name);
        if (it != inventory.end()) {
            it->second.quantity += quantity;
            return true;
        } else {
            return false;
        }
    }

    std::variant<bool, std::string> display_items() {
        if (inventory.empty()) {
            return false;
        } else {
            std::string result;
            for (size_t i = 0; i < order.size(); ++i) {
                if (i > 0) result += "\n";
                const std::string& name = order[i];
                const Item& item = inventory.at(name);
                result += name + " - $" + format_double(item.price) + " [" + std::to_string(item.quantity) + "]";
            }
            return result;
        }
    }
};