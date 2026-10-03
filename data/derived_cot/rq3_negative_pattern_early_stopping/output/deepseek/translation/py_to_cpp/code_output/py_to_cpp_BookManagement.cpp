#include <string>
#include <unordered_map>
#include <vector>
#include <stdexcept>

class BookManagement {
private:
    std::unordered_map<std::string, int> quantities;
    std::vector<std::string> order; // insertion order of keys

public:
    BookManagement() {}

    void add_book(const std::string& title, int quantity = 1) {
        if (quantities.count(title) > 0) {
            quantities[title] += quantity;
        } else {
            quantities[title] = quantity;
            order.push_back(title);
        }
    }

    void remove_book(const std::string& title, int quantity) {
        if (quantities.count(title) == 0 || quantities[title] < quantity) {
            throw false; // mimic Python raising False
        }
        quantities[title] -= quantity;
        if (quantities[title] == 0) {
            quantities.erase(title);
            // remove from order
            for (auto it = order.begin(); it != order.end(); ++it) {
                if (*it == title) {
                    order.erase(it);
                    break;
                }
            }
        }
    }

    // Return a vector of (title, quantity) pairs in insertion order.
    std::vector<std::pair<std::string, int>> view_inventory() const {
        std::vector<std::pair<std::string, int>> result;
        result.reserve(order.size());
        for (const auto& key : order) {
            result.emplace_back(key, quantities.at(key));
        }
        return result;
    }

    int view_book_quantity(const std::string& title) const {
        auto it = quantities.find(title);
        return (it != quantities.end()) ? it->second : 0;
    }
};