#include <unordered_map>
#include <string>

class BookManagement {
private:
    std::unordered_map<std::string, int> inventory;

public:
    BookManagement() = default;

    void add_book(const std::string& title, int quantity = 1) {
        if (inventory.find(title) != inventory.end()) {
            inventory[title] += quantity;
        } else {
            inventory[title] = quantity;
        }
    }

    void remove_book(const std::string& title, int quantity) {
        if (inventory.find(title) == inventory.end() || inventory[title] < quantity) {
            throw false;
        }
        inventory[title] -= quantity;
        if (inventory[title] == 0) {
            inventory.erase(title);
        }
    }

    std::unordered_map<std::string, int> view_inventory() const {
        return inventory;
    }

    int view_book_quantity(const std::string& title) const {
        auto it = inventory.find(title);
        if (it == inventory.end()) {
            return 0;
        }
        return it->second;
    }
};