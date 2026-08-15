#include <string>
#include <unordered_map>
#include <stdexcept>

class BookManagement {
private:
    std::unordered_map<std::string, int> inventory;

public:
    BookManagement() {}

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
        int newQuantity = it->second - quantity;
        if (newQuantity == 0) {
            inventory.erase(it);
        } else {
            it->second = newQuantity;
        }
    }

    std::unordered_map<std::string, int> viewInventory() const {
        return inventory;
    }

    int viewBookQuantity(const std::string& title) const {
        auto it = inventory.find(title);
        return it != inventory.end() ? it->second : 0;
    }
};