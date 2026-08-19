#include <map>
#include <string>
#include <stdexcept>

class BookManagement {
public:
    BookManagement() : inventory() {}

    void add_book(const std::string& title, int quantity = 1) {
        // operator[] default-initializes to 0, so this both creates
        // and increments, matching the Python dict semantics.
        inventory[title] += quantity;
    }

    void remove_book(const std::string& title, int quantity) {
        auto it = inventory.find(title);
        if (it == inventory.end() || it->second < quantity) {
            // Mirrors `raise False`: invalid input raises an error
            // (an exception is thrown, not a bool returned).
            throw std::invalid_argument("Invalid input for remove_book");
        }
        it->second -= quantity;
        if (it->second == 0) {
            inventory.erase(it);
        }
    }

    const std::map<std::string, int>& view_inventory() const {
        // Returns the inventory itself (reference semantics, like Python).
        return inventory;
    }

    int view_book_quantity(const std::string& title) const {
        auto it = inventory.find(title);
        if (it == inventory.end()) {
            return 0;
        }
        return it->second;
    }

private:
    std::map<std::string, int> inventory;
};