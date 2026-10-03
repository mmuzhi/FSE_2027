#include <string>
#include <unordered_map>
#include <stdexcept>

class BookManagement {
private:
    std::unordered_map<std::string, int> inventory;

public:
    BookManagement() = default;

    void addBook(const std::string& title, int quantity) {
        // operator[] inserts a default-initialized value (0 for int) if the key doesn't exist,
        // which perfectly mimics the Java behavior of checking containsKey and then adding.
        inventory[title] += quantity;
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
        // Returning by value creates a copy, identical to `return new HashMap<>(inventory);`
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