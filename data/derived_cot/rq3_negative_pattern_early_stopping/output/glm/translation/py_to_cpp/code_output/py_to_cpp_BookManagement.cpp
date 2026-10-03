#include <string>
#include <map>
#include <stdexcept>

class BookManagement {
private:
    std::map<std::string, int> inventory;

public:
    BookManagement() : inventory() {}

    void add_book(const std::string& title, int quantity = 1) {
        inventory[title] += quantity;
    }

    void remove_book(const std::string& title, int quantity) {
        auto it = inventory.find(title);
        if (it == inventory.end() || it->second < quantity) {
            throw std::runtime_error("Invalid input");
        }
        it->second -= quantity;
        if (it->second == 0) {
            inventory.erase(it);
        }
    }

    std::map<std::string, int> view_inventory() {
        return inventory;
    }

    int view_book_quantity(const std::string& title) {
        auto it = inventory.find(title);
        if (it == inventory.end()) {
            return 0;
        }
        return it->second;
    }
};