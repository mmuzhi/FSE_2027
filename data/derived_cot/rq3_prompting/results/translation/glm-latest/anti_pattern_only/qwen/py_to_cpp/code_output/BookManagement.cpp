#include <map>
#include <string>
#include <stdexcept>

class BookManagement {
public:
    BookManagement() = default;

    // Add one or several books to inventory which is sorted by book title.
    void add_book(const std::string& title, int quantity = 1) {
        // operator[] default-inserts 0 for a new title, so += covers
        // both the "existing" and "new" cases exactly like the Python code.
        inventory[title] += quantity;
    }

    // Remove one or several books from inventory which is sorted by book title.
    // Throws on invalid input (title not present or insufficient quantity),
    // mirroring the Python `raise` on invalid input.
    void remove_book(const std::string& title, int quantity) {
        auto it = inventory.find(title);
        if (it == inventory.end() || it->second < quantity) {
            throw std::invalid_argument("Invalid input: title not in inventory or insufficient quantity");
        }
        it->second -= quantity;
        if (it->second == 0) {
            inventory.erase(it);
        }
    }

    // Get the inventory of the Book Management.
    // Returns a reference to the inventory (key-sorted, like the docstring states).
    const std::map<std::string, int>& view_inventory() const {
        return inventory;
    }

    // Get the quantity of a book.
    // Returns 0 when the title does not exist in the inventory.
    int view_book_quantity(const std::string& title) const {
        auto it = inventory.find(title);
        return it == inventory.end() ? 0 : it->second;
    }

private:
    std::map<std::string, int> inventory;
};