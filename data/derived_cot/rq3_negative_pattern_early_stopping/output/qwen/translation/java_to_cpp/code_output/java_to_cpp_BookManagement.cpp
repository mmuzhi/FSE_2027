#include <unordered_map>
#include <string>
#include <stdexcept>

class BookManagement {
private:
    std::unordered_map<std::string, int> inventory;

public:
    BookManagement() = default;

    void addBook(const std::string& title, int quantity) {
        auto it = inventory.find(title);
        if (it != inventory.end()) {
            it->second += quantity;
        } else {
            inventory.emplace(title, quantity);
        }
    }

    void removeBook(const std::string& title, int quantity) {
        auto it = inventory.find(title);
        if (it == inventory.end() || it->second < quantity) {
            throw std::runtime_error("Invalid operation");
        }
        it->second -= quantity;
        if (it->second == 0) {
            inventory.erase(it);
        }
    }

    std::unordered_map<std::string, int> viewInventory() const {
        return inventory;
    }

    int viewBookQuantity(const std::string& title) const {
        auto it = inventory.find(title);
        if (it != inventory.end()) {
            return it->second;
        }
        return 0;
    }
};