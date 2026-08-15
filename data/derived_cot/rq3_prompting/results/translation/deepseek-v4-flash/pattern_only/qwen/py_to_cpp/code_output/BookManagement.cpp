#include <map>
#include <string>
#include <stdexcept>

class BookManagement {
private:
    std::map<std::string, int> inventory;

public:
    BookManagement() {}

    void add_book(const std::string& title, int quantity = 1) {
        if (inventory.find(title) != inventory.end()) {
            inventory[title] += quantity;
        } else {
            inventory[title] = quantity;
        }
    }

    void remove_book(const std::string& title, int quantity) {
        if (inventory.find(title) == inventory.end() || inventory[title] < quantity) {
            throw std::invalid_argument("False");
        }
        inventory[title] -= quantity;
        if (inventory[title] == 0) {
            inventory.erase(title);
        }
    }

    std::map<std::string, int>& view_inventory() {
        return inventory;
    }

    int view_book_quantity(const std::string& title) {
        if (inventory.find(title) == inventory.end()) {
            return 0;
        }
        return inventory[title];
    }
};